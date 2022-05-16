import xmlrpc.client


class XmlrpcAPI:

    def __init__(self, host, port, db, user, passw):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passw = passw

        root = f"http://{self.host}:{self.port}/xmlrpc/"
        self.uid = xmlrpc.client.ServerProxy(root + "common").login(
            self.db, self.user, self.passw
        )
        self.sock = xmlrpc.client.ServerProxy(root + "object")

    def execute(self, model, method, method_args, *execute_args):
        return self.sock.execute(
            self.db, self.uid, self.passw, model, method, method_args,
            *execute_args
        )


if __name__ == "__main__":
    # Testing ...

    odoo_conexion = dict(
        host="localhost",
        port=8069,
        db="12",
        user="12@",
        passw="12",
    )

    web_service = XmlrpcAPI(**odoo_conexion)

    print("Display all the sessions and their corresponding number of seats.")
    sessions = web_service.execute(model="openacademy.session", method="search_read", method_args=[])

    for session in sessions:
        print(
            "Name session:", session["name"], "Number seats:",
            session["number_seats"]
        )

    print("\nCreate a new session for one of the courses.")
    # First, we create a course:
    course_data = dict(
        name="Mathematics",
        description="Arithmetic and Geometry",
    )
    course_id = web_service.execute(
        model="openacademy.course", method="create", method_args=course_data
    )
    # Second, we created one session for the course:
    session_data = dict(
        name="Session 1",
        number_seats=20,
        course_id=course_id,
    )
    session_id = web_service.execute(
        model="openacademy.session", method="create", method_args=session_data
    )

    # Third, we read the data of the newly created section.
    sessions = web_service.execute(
        model="openacademy.session",
        method="search_read", method_args=[["id", "=", session_id]]
    )

    for session in sessions:
        print(
            "Name session:", session["name"], "Number seats:",
            session["number_seats"]
        )
