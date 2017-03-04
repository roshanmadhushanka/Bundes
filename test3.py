from system.io import FileHandler

file_handler = FileHandler('company_list')
content = file_handler.read()
print content
