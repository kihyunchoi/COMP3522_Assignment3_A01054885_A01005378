import abc


class BaseHandler(abc.ABC):

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abc.abstractmethod
    def handle_request(self, req: Request):
        pass

    def set_handler(self, handler):
        self.next_handler = handler


class ErrorHandler:
    @staticmethod
    def handle_error(error):
        print(error)


class ModeHandler(BaseHandler):

    def handle_request(self, req: Request):
        if req.mode is not None:
            if req.mode == "pokemon" or req.mode == "ability" or req.mode == "move":
                self.set_handler(InputHandler)
                return self.next_handler.handle_request(InputHandler, req)
            else:
                return ErrorHandler.handle_error(f"{req} mode is not provided."
                                                 "Choose one of pokemon | ability | move")
        else:
            return ErrorHandler.handle_error("No mode provided."
                                             " Choose one of pokemon | ability | move")


class InputHandler(BaseHandler):

    def handle_request(self, req: Request):
        if (req.input_file is not None) or (req.input_data is not None):
            self.set_handler(ExpandedHandler)
            return self.next_handler.handle_request(ExpandedHandler, req)
        else:
            return ErrorHandler.handle_error("File or data is not provided")


class ExpandedHandler(BaseHandler):

    def handle_request(self, req: Request):
        if req.expanded is not None:
            if req.expanded == "stats" \
                    or req.expanded == " abilities" \
                    or req.expanded == "moves":
                self.set_handler(OutputHandler)
                return self.next_handler.handle_request(self, req)
            else:
                return ErrorHandler.handle_error(f"{req} mode is not provided."
                                                 "Choose one of stats | abilities | moves")
        else:
            self.set_handler(OutputHandler)
            return None


class OutputHandler(BaseHandler):

    def handle_request(self, req: Request):
        if req.input_file is not None:
            from_file = open(req.input_file, "r")
            from_data = (from_file.read())
            from_file.close()
            if req.output == "print":
                return from_data
            else:
                to_file = open(req.output, "wb")
                result = from_file
                to_file.write(result)
                to_file.close()
                return f"{req.input_file} is Written to {req.output}"
        elif req.input_data is not None:
            from_data = req
            if req.output == "print":
                return from_data
            else:
                to_file = open(req.output, "wb")
                result = from_data
                to_file.write(result)
                to_file.close()
                return f"{req.input_data} is Written to {req.output}"
        else:
            return ErrorHandler.handle_error("Output cannot be provided. "
                                             "No input file or input data")