def get_first_name(full_name):
    return full_name.split(" ")[0]

fallback_name = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name = input("Please enter your name: ")
print('raw name:', raw_name, 'type: ', type(raw_name))
first_name = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name = get_first_name(fallback_name)

print(f"Hi, {first_name}!")
