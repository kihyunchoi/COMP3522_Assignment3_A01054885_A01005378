import des
import argparse
import abc
import enum


# class Expanded(enum.Enum):
#     # Stats
#     STATS = "stats"
#     # Abilities
#     ABILITIES = "abilities"
#     # Moves
#     MOVES = "moves"


class Request:

    def __init__(self):
        self.mode = None
        self.input_file = None
        self.input_data = None
        self.expanded = None
        self.output = None

    def __str__(self):
        return f"Request: Mode: {self.mode}, Input file: {self.input_file}" \
               f", Input data: {self.input_data}, Expanded: {self.expanded}, " \
               f", Output: {self.output}"


def setup_request_commandline() -> Request:
    """
    Implements the argparse module to accept arguments via the command
    line. This function specifies what these arguments are and parses it
    into an object of type Request. If something goes wrong with
    provided arguments then the function prints an error message and
    exits the application.
    :return: The object of type Request with all the arguments provided
    in it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="A positional argument. "
                                     "Choose one of pokemon | ability | move ")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--inputfile",
                       help="A group of mutually exclusive argument. "
                            "This takes a file name (only .txt is accepted)")
    group.add_argument("-d", "--inputdata",
                       help="A group of mutually exclusive argument "
                            "This takes a name(string) or an id(int)")
    parser.add_argument("-ex", "--expanded",
                        help="An optional flag. This supports only pokemon queries. "
                             "This provides more information "
                             "(stats | abilities | moves)")
    parser.add_argument("-o", "--output", default="print",
                        help="The output of the program. This is 'print' by "
                             "default, but can be set to a file name as well.")

    try:
        args = parser.parse_args()
        req = Request()
        req.mode = args.mode
        req.input_file = args.file
        req.input_data = args.inputdata
        req.expanded = args.expanded
        req.output = args.output
        print(req)
        return req
    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()


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


class Aiohttp:

    def __init__(self):
        self.start_handler = ModeHandler()

    def execute_request(self, req: Request):
        result = self.start_handler.handle_request(req)
        print(result)


def main(req: Request):
    aiohttp = Aiohttp()
    aiohttp.execute_request(req)


if __name__ == '__main__':
    request = setup_request_commandline()
    main(request)
