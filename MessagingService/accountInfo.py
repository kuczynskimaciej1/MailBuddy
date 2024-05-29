from dns.resolver import resolve
import requests
import smtplib
import imaplib
import xml.etree.ElementTree as ET


default_settings = {
    'gmail.com': {
        'imap': {'hostname': 'imap.gmail.com', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.gmail.com', 'port': 587, 'socket_type': 'STARTTLS'}
    },
    'yahoo.com': {
        'imap': {'hostname': 'imap.mail.yahoo.com', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.mail.yahoo.com', 'port': 465, 'socket_type': 'SSL'}
    },
    'outlook.com': {
        'imap': {'hostname': 'outlook.office365.com', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.office365.com', 'port': 587, 'socket_type': 'STARTTLS'}
    },
    'poczta.onet.pl': {
        'imap': {'hostname': 'imap.poczta.onet.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.poczta.onet.pl', 'port': 587, 'socket_type': 'STARTTLS'}
    },
    'onet.pl': {
        'imap': {'hostname': 'imap.poczta.onet.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.poczta.onet.pl', 'port': 465, 'socket_type': 'SSL'}
    },
    'wp.pl': {
        'imap': {'hostname': 'imap.wp.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.wp.pl', 'port': 465, 'socket_type': 'SSL'}
    },
    'interia.pl': {
        'imap': {'hostname': 'imap.poczta.interia.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.poczta.interia.pl', 'port': 465, 'socket_type': 'SSL'}
    },
    'pcz.pl': {
        'imap': {'hostname': 'imap.pcz.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.pcz.pl', 'port': 465, 'socket_type': 'SSL'}
    },
    'wimii.pcz.pl': {
        'imap': {'hostname': 'imap.wimii.pcz.pl', 'port': 993, 'socket_type': 'SSL'},
        'smtp': {'hostname': 'smtp.wimii.pcz.pl', 'port': 465, 'socket_type': 'SSL'}
    }
}




def get_domain(email):
    return email.split('@')[1]


def get_mx_records(domain):
    try:
        answers = resolve(domain, 'MX')
        mx_records = [answer.exchange.to_text() for answer in answers]
        return mx_records
    except Exception as e:
        print(f"DNS lookup failed: {e}")
        return []


def get_autodiscover_settings(domain):
    try:
        url = f'https://autoconfig.{domain}/mail/config-v1.1.xml'
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # Process XML to extract settings
        else:
            url = f'https://{domain}/.well-known/autoconfig/mail/config-v1.1.xml'
            response = requests.get(url)
            if response.status_code == 200:
                return response.text  # Process XML to extract settings
    except Exception as e:
        print(f"Autodiscover failed: {e}")
    return None



def parse_email_settings(xml_data):
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    email_provider = root.find('emailProvider')

    settings = {
        'imap': {},
        'pop3': {},
        'smtp': []
    }

    for server in email_provider.findall('incomingServer'):
        server_type = server.get('type')
        settings[server_type] = {
            'hostname': server.find('hostname').text,
            'port': int(server.find('port').text),
            'socket_type': server.find('socketType').text
        }

    for server in email_provider.findall('outgoingServer'):
        smtp_settings = {
            'hostname': server.find('hostname').text,
            'port': int(server.find('port').text),
            'socket_type': server.find('socketType').text
        }
        settings['smtp'].append(smtp_settings)

    return settings



def test_imap_connection(imap_settings, email, password):
    try:
        if imap_settings['socket_type'] == 'SSL':
            connection = imaplib.IMAP4_SSL(imap_settings['hostname'], imap_settings['port'])
        else:
            connection = imaplib.IMAP4(imap_settings['hostname'], imap_settings['port'])
        
        connection.login(email, password)
        connection.logout()
        return True
    except Exception as e:
        print(f"IMAP connection failed: {e}")
        return False


def test_smtp_connection(smtp_settings, email, password):
        try:
            if smtp_settings == 'SSL':
                connection = smtplib.SMTP_SSL(smtp_settings['hostname'], smtp_settings['port'])
            else:
                connection = smtplib.SMTP(smtp_settings['hostname'], smtp_settings['port'])
                if smtp_settings == 'STARTTLS':
                    connection.starttls()

            connection.login(email, password)
            connection.quit()
            return True
        except Exception as e:
            print(f"SMTP connection to {smtp_settings['hostname']} on port {smtp_settings['port']} failed: {e}")
        return False


def discover_email_settings(email, password):
    domain = get_domain(email)
    
    mx_records = get_mx_records(domain)
    print(mx_records)
    if mx_records:
        pass
    
    # Try autodiscovery
    settings_xml = get_autodiscover_settings(domain)
    if settings_xml:
        settings_xml = parse_email_settings(settings_xml)
        pass
    
    # Use default settings
    if domain in default_settings:
        settings_xml = default_settings[domain]
        print(settings_xml)
    else:
        print("No settings found for this domain.")
    
    # Test IMAP and SMTP connections
    if test_imap_connection(settings_xml['imap'], email, password) and test_smtp_connection(settings_xml['smtp'], email, password):
        print("Check ok")
        print(settings_xml)
        return settings_xml
    else:
        print("Failed to connect with discovered settings.")
        return None