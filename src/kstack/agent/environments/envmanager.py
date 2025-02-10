import json
import os

from kstack.agent import settings


class KstackEnvironment:

    def __init__(self, hostname):
        self.hostname = hostname


    def __str__(self):
        return f"{self.hostname}"


    def __repr__(self):
        return f"{self.hostname}"


    def to_dict(self):
        return {
            "hostname": self.hostname,
            #"hostname": self.hostname,
            #"id": self.id,
            #"ip": self.ip,
            #"description": self.description,
            #"status": self.status
        }


class EnvManager:
    envs = list()

    @classmethod
    def enumerate_environments(cls) -> list:
        cls.envs = list()

        # always add local machine
        localenv = KstackEnvironment("localhost")
        cls.envs.append(localenv)

        # lookup other environments using the available env enumerators
        # built-in enumerator: find 'env.json' files in subdirectories of the data/environments directory
        envs_base_dir = f"{settings.AGENT_DATA_DIR}/environments"
        os.makedirs(envs_base_dir, exist_ok=True)

        for env_dir in os.listdir(envs_base_dir):
            if os.path.isdir(f"{envs_base_dir}/{env_dir}"):
                env_file = f"{envs_base_dir}/{env_dir}/env.json"
                if os.path.exists(env_file):
                    # with open(env_file, "r") as f:
                    #     env_data = json.load(f)
                    #     env = KstackEnvironment(env_data["hostname"])
                    #     cls.envs.append(env)
                    cls.envs.append(KstackEnvironment(env_dir))

        return cls.envs


    @classmethod
    def list_environments(cls) -> list:
        return cls.envs


    @classmethod
    def create(cls, env: KstackEnvironment) -> KstackEnvironment:
        # check if env already exists
        for _env in cls.envs:
            if _env.hostname == env.hostname:
                raise Exception(f"Environment with hostname {env.hostname} already exists")

        # create the environment directory and save the env.json file
        env_dir = f"{settings.AGENT_DATA_DIR}/environments/{env.hostname}"
        os.makedirs(env_dir, exist_ok=True)

        env_file = f"{env_dir}/env.json"
        with open(env_file, "w") as f:
            json.dump(env.to_dict(), f, indent=4)

        cls.envs.append(env)
        return env


    @classmethod
    def get(cls, hostname) -> KstackEnvironment | None:
        for env in cls.envs:
            if env.hostname == hostname:
                return env
        return None


    @classmethod
    def remove(cls, hostname) -> KstackEnvironment | None:
        for env in cls.envs:
            if env.hostname == hostname:
                # just rename the env.json file to env.deleted.json
                env_dir = f"{settings.AGENT_DATA_DIR}/environments/{env.hostname}"
                os.rename(f"{env_dir}/env.json", f"{env_dir}/env.deleted.json")

                cls.envs.remove(env)
                return env
        return None


    @classmethod
    def reset(cls):
        cls.envs = list()


    # @classmethod
    # def get_by_id(cls, id) -> KstackEnvironment:
    #     for env in cls.envs:
    #         if env.id == id:
    #             return env
    #     return None