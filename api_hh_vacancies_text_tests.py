import requests, lorem

url_base = "https://api.hh.ru/vacancies?text="

token = input( "Введите токен: " )

headers = {
  'Authorization': 'Bearer ' + token
}

def get_response_with_testing_param(test):
	return requests.request("GET", url_base + test, headers=headers)

def find_if_next_symbols_after_sub_diff(main_str, sub):
	answer = False
	start = main_str.find(sub, 0)
	if start == -1: return answer
	a = main_str[start + len(sub)]	
	while True:
		start = main_str.find(sub, start)
		if start == -1: return
		if a != main_str[start  + len(sub)]: 
			answer = True
			break
		start += len(sub)
	return answer

# general tests in 'text' param:

def test_wrong_spelling_Status_code_equals_200():
	test_text = 'москьва'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_wrong_spelling_Get_right_answer():
	test_text = 'москьва'
	response = get_response_with_testing_param(test_text)
	assert response.text.find('Москва') != -1

def test_magic_several_params_Status_code_equals_200():
	test_text = 'бухгалтер омск 15000'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_magic_several_params_Magic_works():
	test_text = 'бухгалтер омск 15000'
	response = get_response_with_testing_param(test_text)
	# if we got separate params in alternate_url then magic works
	assert response.json()['alternate_url'].find('salary=15000') != -1 and response.json()['alternate_url'].find('text=%D0%B1%D1%83%D1%85%D0%B3%D0%B0%D0%BB%D1%82%D0%B5%D1%80') != -1 and response.json()['alternate_url'].find('area=68') != -1

def test_too_many_symbols_Status_code_equals_502():
	test_text = lorem.return_lorem(4500)
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 502 # 502 - OK for too long text.

def test_text_equals_null_Status_code_equals_200():
	test_text = 'null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_text_empty_two_quotes_Status_code_equals_200():
	test_text = ''
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_text_non_ASCII_Status_code_equals_200():
	test_text = 'भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_text_correct_Status_code_equals_200():
	test_text = 'уборщик'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_text_correct_Get_right_answer():
	test_text = 'уборщик'
	response = get_response_with_testing_param(test_text)
	assert response.text.find('уборщик') != -1

# search language tests:

def test_text_synonym_Get_right_answer():
	test_text = 'пиарщик'
	response = get_response_with_testing_param(test_text)
	assert response.text.find('PR') != -1

def test_text_part_of_word_Get_right_answer():
	test_text = 'Гео*'
	response = get_response_with_testing_param(test_text)
	assert find_if_next_symbols_after_sub_diff(response.text, 'Гео')

def test_text_AND_Get_right_answer():
	test_text = '!уборщик AND !клинер'
	response = get_response_with_testing_param(test_text)
	first_item = str(response.json()['items'][0]).lower()
	assert first_item.find('уборщик') != -1 and first_item.find('клинер') != -1

def test_text_NOT_Get_right_answer():
	test_text = 'клининг NOT уборщик'
	response = get_response_with_testing_param(test_text)
	assert response.text.lower().find('уборщик') == -1

def test_text_OR_Get_right_answer():
	test_text = 'клининг OR уборщик'
	response = get_response_with_testing_param(test_text)
	assert response.text.lower().find('уборщик') != -1 and response.text.find('клининг') != -1

def test_text_find_phrase_Get_right_answer():
	test_text = 'холодные звонки'
	response = get_response_with_testing_param(test_text)
	assert response.text.lower().find('холодные звонки') != -1

# search by fields tests:

#!ID:

def test_ID_equals_null_Status_code_equals_200():
	test_text = '!ID:null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_empty_two_quotes_Status_code_equals_200():
	test_text = '!ID:""'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_negative_num_Status_code_equals_200():
	test_text = '!ID:-1'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_positive_num_incorrect_Status_code_equals_200():
	test_text = '!ID:100'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_positive_num_correct_Status_code_equals_200():
	test_text = '!ID:41029616'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_russian_text_Status_code_equals_200():
	test_text = '!ID:админ'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_english_text_Status_code_equals_200():
	test_text = '!ID:admin'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200
# next test fails, we can see 
def test_ID_non_ASCII_Status_code_equals_200():
	test_text = '!ID:भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_ID_no_exclamation_mark_Status_code_equals_502():
	test_text = 'ID:41029616'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 502

# !COMPANY_ID:

def test_COMPANY_ID_equals_null_Status_code_equals_200():
	test_text = '!COMPANY_ID:null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_empty_two_quotes_Status_code_equals_200():
	test_text = '!COMPANY_ID:""'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_negative_num_Status_code_equals_200():
	test_text = '!COMPANY_ID:-1'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_positive_num_incorrect_Status_code_equals_200():
	test_text = '!COMPANY_ID:100'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_positive_num_correct_Status_code_equals_200():
	test_text = '!ID:2067747'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_russian_text_Status_code_equals_200():
	test_text = '!COMPANY_ID:админ'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_english_text_Status_code_equals_200():
	test_text = '!COMPANY_ID:admin'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_ID_non_ASCII_Status_code_equals_200():
	test_text = '!COMPANY_ID:भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

# NAME:

def test_NAME_equals_null_Status_code_equals_200():
	test_text = 'NAME:null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_NAME_empty_two_quotes_Status_code_equals_200():
	test_text = 'NAME:""'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_NAME_non_ASCII_Status_code_equals_200():
	test_text = 'NAME:भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_NAME_correct_Status_code_equals_200():
	test_text = 'NAME:уборщик'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_NAME_correct_Get_right_answer():
	test_text = 'NAME:!уборщик'
	response = get_response_with_testing_param(test_text)
	first_item_name = str(response.json()['items'][0]['name']).lower()
	assert first_item_name.find('уборщик') != -1

# COMPANY_NAME

def test_COMPANY_NAME_equals_null_Status_code_equals_200():
	test_text = 'COMPANY_NAME:null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_NAME_empty_two_quotes_Status_code_equals_200():
	test_text = 'COMPANY_NAME:""'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_NAME_non_ASCII_Status_code_equals_200():
	test_text = 'COMPANY_NAME:भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_NAME_correct_Status_code_equals_200():
	test_text = 'COMPANY_NAME:Газпром'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_COMPANY_NAME_correct_Get_right_answer():
	test_text = 'COMPANY_NAME:Газпром'
	response = get_response_with_testing_param(test_text)
	first_item_company_name = str(response.json()['items'][0]['employer']['name']).lower()
	assert first_item_company_name.find('газпром') != -1	

# DESCRIPTION

def test_DESCRIPTION_equals_null_Status_code_equals_200():
	test_text = 'DESCRIPTION:null'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_DESCRIPTION_empty_two_quotes_Status_code_equals_200():
	test_text = 'DESCRIPTION:""'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_DESCRIPTION_non_ASCII_Status_code_equals_200():
	test_text = 'DESCRIPTION:भारत'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200

def test_DESCRIPTION_correct_Status_code_equals_200():
	test_text = 'DESCRIPTION:Компания'
	response = get_response_with_testing_param(test_text)
	assert response.status_code == 200