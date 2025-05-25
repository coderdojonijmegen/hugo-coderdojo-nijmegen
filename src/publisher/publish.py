from dotenv import load_dotenv

from env import Environment

load_dotenv()

if __name__ == "__main__":
    env = Environment.load()
    print(env)

