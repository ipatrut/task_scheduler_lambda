from localstack.utils.aws import aws_stack
from localstack.utils import testutil
from localstack.utils.common import load_file
from localstack.services.awslambda.lambda_api import LAMBDA_RUNTIME_PYTHON36

from localstack.services import infra

logger = logging.getLogger()
logger.setLevel(logging.INFO)

my_env = os.environ.copy()
my_env["SERVICES"] = "serverless"  # can probably change this to "lambda,sns"
my_env["DEBUG"] = "1"
my_env["LAMBDA_EXECUTOR"] = "local"

os.environ["AWS_ACCESS_KEY_ID"] = "foo"
os.environ["AWS_SECRET_ACCESS_KEY"] = "foo"

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
TEST_LAMBDA_NAME_PY3 = 'test_lambda_py3'
TEST_LAMBDA_PYTHON3 = os.path.join(THIS_FOLDER, 'lambdas', 'lambda_python3.py')
TEST_LAMBDA_LIBS = ['localstack', 'localstack_client', 'requests',
                    'psutil', 'urllib3', 'chardet', 'certifi', 'idna', 'pip',
                    'dns']


class TestBasic(unittest.TestCase):
    def setUp(self):
        infra.start_lambda(asynchronous=True)
        infra.start_cloudwatch(asynchronous=True)

    def test_run_lambda(self):
        zip_file = testutil.create_lambda_archive(
            load_file(TEST_LAMBDA_PYTHON3),
            get_content=True,
            libs=TEST_LAMBDA_LIBS,
            runtime=LAMBDA_RUNTIME_PYTHON36)

        testutil.create_lambda_function(
            func_name=TEST_LAMBDA_NAME_PY3,
            zip_file=zip_file,
            runtime=LAMBDA_RUNTIME_PYTHON36
        )

        lambda_client = aws_stack.connect_to_service('lambda')

        result = lambda_client.invoke(
            FunctionName=TEST_LAMBDA_NAME_PY3, Payload=b'{}')

        self.assertEqual(result['StatusCode'], 200)

    def teardown(self):
        pass


if __name__ == '__main__':
    unittest.main()