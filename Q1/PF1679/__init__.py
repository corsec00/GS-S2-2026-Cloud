import logging
import os
import socket

import azure.functions as func


def check_server(host, port):

    try:
        with socket.create_connection(
            (host, port),
            timeout=3
        ):
            return True

    except:
        return False


def main(timer: func.TimerRequest) -> None:

    servers = os.getenv("SERVERS")

    if not servers:
        logging.error("Variável SERVERS não encontrada.")
        return

    server_list = [
        s.strip()
        for s in servers.split(",")
    ]

    logging.info("Iniciando monitoramento...")

    for server in server_list:

        host, port = server.split(":")
        port = int(port)

        if check_server(host, port):

            logging.info(
                f"[ONLINE] {host}:{port}"
            )

        else:

            logging.warning(
                f"[OFFLINE] {host}:{port}"
            )

    logging.info("Monitoramento finalizado.")
