import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
user_profile = input("> Give your profile name: ")
if user_profile == "":
    user_profile = "Default"
dotenv.set_key(dotenv_file, "CHROME_PROFILE", user_profile)
print(
    f'Please Login into ChatGPT from "{user_profile}" and complete all human verification steps!'
)
