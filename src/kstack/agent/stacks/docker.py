import json
import os
import shutil
import subprocess

from docker.constants import DEFAULT_TIMEOUT_SECONDS

from kstack.agent.stacks import ContainerStack
from kstack.agent.util.subprocess_util import kwargs_to_cmdargs, load_envfile

class DockerComposeStack(ContainerStack):
    def __init__(self, name, managed=False, meta=None, **kwargs):
        super().__init__(name, managed=managed, meta=meta)


    # @staticmethod
    # def _map_kwargs(kwargs):
    #     """
    #     Map kwargs to docker compose arguments
    #     :param kwargs:
    #     :return:
    #     """
    #     args = []
    #     for k, v in kwargs.items():
    #         if v is not None and v is not False:
    #             if len(k) == 1 and type(v) is bool:
    #                 args.append(f"-{k}")
    #                 continue
    #
    #             args.append(f"--{k.replace('_', '-')}")
    #             if type(v) is not bool:
    #                 args.append(str(v))
    #     return args


    def _compose(self, cmd, **kwargs) -> bytes:
        """
        Run a docker compose command
        :param cmd: Command to run
        :param kwargs: Additional arguments to pass to docker compose
        :return:
        """
        compose_args = {}
        compose_args['project-name'] = self.name
        #compose_args['project-directory'] = self.project_dir
        #compose_args['file'] = 'docker-compose.yml'
        #compose_args['progress'] = 'auto'

        working_dir = self.project_dir
        if self.meta:
            base_path = self.meta.get('base_path', "")
            working_dir = os.path.join(self.project_dir, base_path)

        try:
            pcmd = ((["docker", "compose"]
                    + kwargs_to_cmdargs(compose_args)) # compose specific args
                    + [cmd] # the compose command (up/down/...)
                    + kwargs_to_cmdargs(kwargs)) # additional command args
            print(f"RAW CMD: {pcmd}")
            print(f"CMD: {" ".join(pcmd)}")

            #penv = os.environ.copy()
            penv = dict()
            penv['PATH'] = os.getenv('PATH')
            penv['COMPOSE_PROJECT_NAME'] = self.name
            penv['COMPOSE_FILE'] = 'docker-compose.yml'
            penv['COMPOSE_PROJECT_DIRECTORY'] = working_dir
            penv['PWD'] = working_dir
            #penv['DOCKER_HOST'] = 'unix:///var/run/docker.sock'

            # Load .env file into 'penv'
            env_file = os.path.join(working_dir, '.env')
            if os.path.exists(env_file):
                penv = load_envfile(env_file, penv)
            print(f"ENV: {penv}")

            p1 = subprocess.run(pcmd, cwd=working_dir, env=penv, capture_output=True)
            print("STDOUT", p1.stdout)
            print("STDERR", p1.stderr)

            if p1.returncode != 0:
                raise Exception(f"Error running command: {p1.stderr}")

            return p1.stdout
        except Exception as e:
            print(e)
            raise e


    @property
    def status(self) -> dict:
        """
        Get the status of the stack
        """
        status = dict({
            "name": self.name,
            "project_dir": self.project_dir,
            "managed": self.managed,
            "has_docker_compose": os.path.exists(os.path.join(self.project_dir, "docker-compose.yml")),
            "has_stack_file": os.path.exists(self.project_file),
            "has_stack": os.path.exists(self.project_dir)
        })
        return status

    # @property
    # def meta(self):
    #     # read the stack file contents
    #     meta = dict()
    #     if os.path.exists(self.project_file):
    #         with open(self.project_file, "r") as f:
    #             meta = json.load(f)
    #
    #     return meta


    def up(self, **kwargs) -> bytes:
        """
        Start the stack
        https://docs.docker.com/reference/cli/docker/compose/up/

        Runs docker compose up

        :param kwargs: Additional arguments to pass to docker compose up
        """
        print(f"Starting project {self.name} in {self.project_dir}")

        kwargs['detach'] = True if 'detach' not in kwargs else kwargs['detach']
        kwargs['build'] = True if 'build' not in kwargs else kwargs['build']
        kwargs['force-recreate'] = True if 'force-recreate' not in kwargs else kwargs['force-recreate']
        #kwargs['y'] = True if 'y' not in kwargs else kwargs['y'] # run non-interactively

        return self._compose("up", **kwargs)


    def down(self, **kwargs) -> bytes:
        """
        Remove the stack.

        Runs docker compose down

        :param kwargs: Additional arguments to pass to docker compose down
        """
        print(f"COMPOSE DOWN {self.name} in {self.project_dir}")

        kwargs['timeout'] = DEFAULT_TIMEOUT_SECONDS if 'timeout' not in kwargs else kwargs['timeout']
        return self._compose("down", **kwargs)


    def stop(self, **kwargs) -> bytes:
        """
        Stop the stack.

        Runs docker compose stop

        :param kwargs: Additional arguments to pass to docker compose stop
        """
        print(f"COMPOSE STOP {self.name} in {self.project_dir}")

        kwargs['timeout'] = DEFAULT_TIMEOUT_SECONDS if 'timeout' not in kwargs else kwargs['timeout']
        return self._compose("stop", **kwargs)


    def restart(self, **kwargs) -> bytes:
        print(f"COMPOSE RESTART {self.name} in {self.project_dir}")

        # Run docker compose restart
        kwargs['timeout'] = DEFAULT_TIMEOUT_SECONDS if 'timeout' not in kwargs else kwargs['timeout']
        return self._compose("restart", **kwargs)


    def destroy(self, **kwargs) -> bytes:
        #print(f"COMPOSE DESTROY {self.name} in {self.project_dir}")
        # No docker-specific destroy actions needed.
        # Just remove the project directory and the project file using the stack manager.
        pass


    def ps(self, **kwargs) -> bytes:
        """
        Get the status of the stack

        Runs docker compose ps

        :param kwargs: Additional arguments to pass to docker compose ps
        """
        return self._compose("ps", **kwargs)


    # def serialize(self) -> dict:
    #     return {
    #         "name": self.name,
    #         "project_dir": self.project_dir,
    #         "managed": self.managed
    #     }
    #
    # def to_dict(self):
    #     return self.serialize()

    # @classmethod
    # def from_docker_compose(cls, project, docker_compose_path):
    #     # Read the file path contents
    #     with open(docker_compose_path, "r") as f:
    #         contents = f.read()
    #
    #     p = cls(project, contents)
    #     return p
    #
    # @classmethod
    # def from_json(cls, data):
    #     return cls(data['name'], data['attrs'])
