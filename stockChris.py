import smtplib
from email.mime.text import MIMEText
import http.client
import json

def API(sql, headers):
    """
    This function connects to the sql database and retrieves the stocks data.
    :param sql:
    :return: a data dictionary
    """
    conn = http.client.HTTPSConnection("hotstoks-sql-finance.p.rapidapi.com")

    # python: get data from website
    conn.request("POST", "/query", sql, headers)
    res = conn.getresponse()

    # reading
    data = res.read()
    # decoding
    data = data.decode("utf-8")
    # convert to dictionary
    data = json.loads(data)

    return data

def create_sql(symbol):
    '''
    This function this function takes a stock ticker symbol, inserts it in SQL and returns the text.

    :param symbol: stock ticker (ex. AMZN, AAPL)
    :return: it returns the sql data
    '''

    sql_string = """
    SELECT name, price, pe_ratio
    FROM stocks
    WHERE symbol = '""" + symbol + """'"""

    return sql_string

def generate_email_text(stock_data):
    """
    creates a user friendly string representing the content of an email given input a dictionary (not user friendly)

    :param stock_data:
    :return:
    """
    results = stock_data["results"]
    firststock = results[0]
    peratio = firststock["pe_ratio"]
    price = firststock["price"]
    price = float(price)
    name = firststock["name"]

    email_content = f"""
    Hello investor,\n
    You have selected the {name} stock and you set an alert for when it will reach x pe ratio. 
        * price of  stock is {price}
        * pe ratio is {peratio}. 
    """
    return email_content

def send_email(email_content_text, me, password, you):
    email_template = MIMEText(email_content_text)

    email_template["From"] = me
    email_template["To"] = ",".join(you)
    email_template["Subject"] = "Hello there"

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(me, password)
    s.sendmail(me, you, email_template.as_string())
    s.quit()

if __name__ == '__main__':
    headers = {
        'content-type': "text/plain",
        'X-RapidAPI-Host': "hotstoks-sql-finance.p.rapidapi.com",
        'X-RapidAPI-Key': "f3e259d6damshb4ef9605aa104b4p1efaccjsne0bcdc9b3c67"
    }
    symbol = input("Enter stock symbol: ")
    sql = create_sql(symbol)
    stock_data = API(sql, headers)
    email_content_text = generate_email_text(stock_data)
    me = input("Enter your email address: ")
    password = input("Enter your email password: ")
    you = input("Enter recipient email address (separated by commas if multiple): ").split(',')
    send_email(email_content_text, me, password, you)
