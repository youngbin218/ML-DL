import ssl
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime, timedelta

members_id = ["lCan37", "soline013", "Hayeon-Lee", "yeilin-dpfls", "gPdnjs", "KangDaegyeom", "youngbin218", "dn5772", "yuris99"]
members_name = ["지석훈", "심현솔", "이하연", "최예린", "신혜원", "강대겸", "기영빈", "신대니", "홍지훈"]
# "Bisu-tjdgus", "wjdwns"
# "조성현", "박정준"
                
app = Flask(__name__)

@app.route('/')
@app.route('/check',methods=['POST'])
def check(start_date=None, end_date=None, cnt=[], penalty=[], name=None):
    if request.method != 'POST' and start_date == None and end_date == None:
        return render_template('main.html', start_date=start_date, end_date=end_date, cnts=cnt, penaltys=penalty, names=members_name, zip=zip)
    
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        cnt = []
        penalty = []
        url = "https://github.com"
        day = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
        for i in range(0,9):
            not_commit_cnt = 0
            member_url = url + "/" + members_id[i]
            res = urllib.request.urlopen(member_url)
            soup = BeautifulSoup(res, "html.parser")

            results = soup.select("div.position-relative svg g")

            tmp = 0
            for result in results:
                if tmp == 1:
                    break
                git_commit = result.select("rect")
                if git_commit[0]["data-date"] < end_date:
                    for j in range(1,6):
                        if git_commit[j]["data-date"] == day:
                            if int(git_commit[j]["data-count"]) == 0:
                                not_commit_cnt += 1
                            tmp = 1
                            break
                        elif start_date <= git_commit[j]["data-date"] <= end_date:
                            if int(git_commit[j]["data-count"]) == 0:
                                not_commit_cnt += 1
                        elif git_commit[j]["data-date"] > end_date:
                            break
                else:
                    break
                    
            member_price = 0
            if 3 < not_commit_cnt <= 8:
                member_price = 2500 * 2 ** (not_commit_cnt - 4)
            # if 5 < not_commit_cnt <= 10:
                #member_price = 2500 * 2 ** (not_commit_cnt - 6)
            elif not_commit_cnt >= 9:
                member_price = 50000
            
            cnt.append(not_commit_cnt)
            penalty.append(member_price)
    else:
        start_date = None
        end_date = None
        cnt = []
        penalty = []
        
    return render_template('main.html', start_date=start_date, end_date=end_date, cnts=cnt[:], penaltys=penalty[:], names=members_name, zip=zip)

if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='')
    app.run(host='0.0.0.0', port='5000', threaded=True, ssl_context=ssl_context)
