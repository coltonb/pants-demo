from pants_demo.lambdas.demo_lambda.container import Container

container = Container()
event_handler = container.event_handler()


def lambda_handler(event, _context):
    event_handler.handle_event(event)
