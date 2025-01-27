from cleo.commands.command import Command
from cleo.helpers import argument, option


class ServeCommand(Command):
    name = "serve"

    description = "Start a model serving."

    arguments = [argument("model_name", "The name of the model to serve.")]
    options = [
        option(
            'grpc_port',
            None,
            'The gRPC port to serve the model on.',
            flag=False,
            default=51001,
        ),
        option(
            'http_port',
            None,
            'The HTTP port to serve the model on.',
            flag=False,
            default=51002,
        ),
        option('enable_cors', None, 'Enable CORS.', flag=True),
        option(
            'precision', None, 'The precision of the model.', flag=False, default='fp16'
        ),
        option(
            'device_map',
            None,
            'The device map of the model.',
            flag=False,
            default='balanced',
        ),
        option(
            "replicas", "r", "The number of replicas to serve.", flag=False, default=1
        ),
    ]

    help = """\
    This command allows you to start a model serving in protocol gRPC and HTTP.
    
    To start a model serving, you can run:
        
        <comment>opengpt serve facebook/llama-7b</comment>"""

    def handle(self) -> int:
        from open_gpt.factory import create_flow

        with create_flow(
            self.argument('model_name'),
            grpc_port=self.option('grpc_port'),
            http_port=self.option('http_port'),
            cors=self.option('enable_cors'),
            uses_with={
                'precision': self.option('precision'),
                'device_map': self.option('device_map'),
            },
            replicas=self.option('replicas'),
        ) as flow:
            self.line(
                f'<info>The model is ready to be used at port {self.option("grpc_port")} (gRPC) and {self.option("http_port")} (HTTP).</info>'
            )
            flow.block()

        return 0
