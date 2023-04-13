from server import create_app
from email_utils import send_email

KATHI_ID = '100009018941268'

send_email('diegocerdan@gmail.com', 'Launching Facebook Comments Bot', '')

def handle_comment_event(data):
    #from pprint import pprint
    #pprint(data)

    if(data['verb'] == 'add' and 'message' in data):
        print(data['from']['name'] + ': ' + data['message'])
        print(data['post']['permalink_url'].replace('https://www.', 'https://').replace('?type=3', ''))

    print('')

app = create_app(handle_comment_event)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
