import argparse
import os
from pprint import pprint
import requests


class ServiceNowUpdater:
    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_ticket_details(self, ticket_type: str, ticket_id: str) -> dict:
        r = requests.get(
            f"{self.base_url}/api/now/v1/table/{ticket_type}/{ticket_id}",
            auth=(self.username, self.password),
        )
        return r.json()["result"]

    def get_request_details(self, request_id: str) -> dict:
        return self.get_ticket_details("sc_req_item", request_id)

    def request_is_open(self, request_id: str) -> bool:
        return self.get_request_details(request_id)["state"] == "1"

    def add_ticket_comment(
        self, ticket_type: str, ticket_id: str, comment: str
    ) -> None:
        r = requests.patch(
            f"{self.base_url}/api/now/v1/table/{ticket_type}/{ticket_id}",
            auth=(self.username, self.password),
            json={"comments": comment},
        )
        r.raise_for_status()

    def add_ticket_work_notes(
        self, ticket_type: str, ticket_id: str, work_notes: str
    ) -> None:
        r = requests.patch(
            f"{self.base_url}/api/now/v1/table/{ticket_type}/{ticket_id}",
            auth=(self.username, self.password),
            json={"work_notes": work_notes},
        )
        r.raise_for_status()

    def add_request_comment(self, request_id: str, comment: str) -> None:
        self.add_ticket_comment("sc_req_item", request_id, comment)

    def add_request_work_notes(self, request_id: str, work_notes: str) -> None:
        self.add_ticket_work_notes("sc_req_item", request_id, work_notes)

    def update_request_variables(self, request_id: str, variable_dict: dict) -> None:
        r = requests.put(
            f"{self.base_url}/api/x_tamu2_aip_cloud/ritm_variable_updates?ritm_id={request_id}",
            auth=(self.username, self.password),
            json={"variables": variable_dict},
        )
        r.raise_for_status()
        pprint(r.json())

    def update_request_variable(
        self, request_id: str, variable_name: str, variable_value: str
    ) -> None:
        self.update_request_variables(request_id, {variable_name: variable_value})

    def close_ticket(self, ticket_type: str, ticket_id: str) -> None:
        r = requests.patch(
            f"{self.base_url}/api/now/v1/table/{ticket_type}/{ticket_id}",
            auth=(self.username, self.password),
            json={"state": "3"},
        )
        r.raise_for_status()

    def close_request(self, request_id: str) -> None:
        self.close_ticket("sc_req_item", request_id)


def main():

    assert "SN_BASE_URL" in os.environ, "SN_BASE_URL not set"
    assert "SN_USERNAME" in os.environ, "SN_USERNAME not set"
    assert "SN_PASSWORD" in os.environ, "SN_PASSWORD not set"

    sn_updater = ServiceNowUpdater(
        os.environ["SN_BASE_URL"], os.environ["SN_USERNAME"], os.environ["SN_PASSWORD"]
    )

    parser = argparse.ArgumentParser()

    parser.add_argument("--request_id", help="ServiceNow request ID", required=True)
    subparsers = parser.add_subparsers(help="Action to perform")
    group_comment = subparsers.add_parser('add_comment', help="Add comment to request")
    group_comment.add_argument(
        "--comment", help="Comment to add to request", required=False
    )
    group_work_notes = subparsers.add_parser('add_work_notes', help="Add work notes to request")
    group_work_notes.add_argument(
        "--work_notes", help="Work notes to add to request", required=False
    )
    group_update_variable = subparsers.add_parser('update_request_variable', help="Update request variable")
    group_update_variable.add_argument(
        "--variable_name", help="Variable name to update", required=False
    )
    group_update_variable.add_argument(
        "--variable_value", help="Variable value to update", required=False
    )

    group_close_request = subparsers.add_parser('close_request', help="Close request")
    group_close_request.add_argument(
        "--close", help="Close request", action="store_true"
    )

    args = parser.parse_args()

    if 'comment' in args:
        sn_updater.add_request_comment(args.request_id, args.comment)
    elif 'work_notes' in args:
        sn_updater.add_request_work_notes(args.request_id, args.work_notes)
    elif 'variable_name' in args and 'variable_value' in args:
        sn_updater.update_request_variable(
            args.request_id, args.variable_name, args.variable_value
        )
    elif 'close' in args:
        sn_updater.close_request(args.request_id)
    else:
        raise ValueError("No action specified")


if __name__ == "__main__":
    main()
