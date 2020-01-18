from argparse import ArgumentParser

from Common.HttpFileManager.webApplication import app


def parse_args():
	parser = ArgumentParser()
	parser.add_argument("-i", "--hostname", dest="HOSTNAME", default='localhost',
						help="ip of server host.")
	parser.add_argument("-p", "--port", dest="PORT", default=5000, type=int,
						help="used port for server.")
	return parser.parse_args()


# Main.
if __name__ == '__main__':
	args = parse_args()
	app.run(host=args.HOSTNAME, port=args.PORT, debug=True)