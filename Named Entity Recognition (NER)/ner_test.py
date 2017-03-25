import matplotlib.pyplot as plt
import re
import json
plt.close("all")


def threshold(num, total):
    outcome = [individual for individual in total if individual[2] >= num]
    return outcome

total_list = [['Samsung', 'ORGANIZATION', 112], ['U.S.', 'LOCATION', 50], ['ISS', 'ORGANIZATION', 18], ['Europe', 'LOCATION', 7], ['Korea', 'LOCATION', 64], ['AP', 'ORGANIZATION', 35], ['Bloomberg', 'ORGANIZATION', 33], ['Kospi', 'LOCATION', 1], ['Kwon Oh-hyun', 'PERSON', 9], ['Kwon', 'PERSON', 2], ['Lee Jae-yong', 'PERSON', 2], ['Jay Y.', 'PERSON', 7], ['Suwon', 'LOCATION', 14], ['Fiat', 'ORGANIZATION', 4], ['Marelli', 'LOCATION', 3], ['Marelli', 'PERSON', 2], ['Ferrari NV', 'ORGANIZATION', 1], ['New York Stock Exchange', 'ORGANIZATION', 1], ['Ferrari', 'PERSON', 1], ['Pietro Gorlier', 'PERSON', 1], ['Sergio Marchionne', 'PERSON', 2], ['Milan', 'LOCATION', 1], ['General Motors Co.', 'ORGANIZATION', 4], ['Marchionne', 'PERSON', 2], ['Lee', 'PERSON', 38], ['Asia', 'LOCATION', 13], ['Lotte Group', 'ORGANIZATION', 7], ['Lotte', 'PERSON', 5], ['Japan', 'LOCATION', 9], ['Park Chung-hee', 'LOCATION', 1], ['International Monetary Fund', 'ORGANIZATION', 1], ['Paul Elliott Singer', 'PERSON', 23], ['Lotte', 'LOCATION', 4], ['Hong Kong', 'LOCATION', 10], ['Orix Corp.', 'ORGANIZATION', 1], ['Cnooc Ltd.', 'ORGANIZATION', 1], ['China', 'LOCATION', 13], ['Canon', 'ORGANIZATION', 1], ['Tokyo', 'LOCATION', 2], ['Taiwan', 'LOCATION', 2], ['Fed', 'ORGANIZATION', 10], ['Chris Weston', 'PERSON', 1], ['IG Ltd.', 'ORGANIZATION', 2], ['Melbourne', 'LOCATION', 2], ['Fujitsu Ltd.', 'ORGANIZATION', 1], ['Bank of Japan', 'ORGANIZATION', 2], ['China Petroleum & Chemical Corp.', 'ORGANIZATION', 1], ['PetroChina Co.', 'ORGANIZATION', 1], ['Shanghai', 'LOCATION', 2], ['Tata Motors Ltd.', 'ORGANIZATION', 1], ['Mumbai', 'LOCATION', 1], ['Tata Group', 'ORGANIZATION', 1], ['Cyrus Mistry', 'PERSON', 1], ['US', 'LOCATION', 11], ['S&P', 'ORGANIZATION', 2], ['New Zealand', 'LOCATION', 2], ['Philippine Stock Exchange Index', 'ORGANIZATION', 1], ['Seoul', 'LOCATION', 43], ['Lee Kun-hee', 'PERSON', 16], ['Lee Chaiwon', 'PERSON', 1], ['Korea Value Asset Management Co.', 'ORGANIZATION', 2], ['Elliott Management', 'ORGANIZATION', 13], ['Paul Singer', 'PERSON', 2], ['Heo Pil-seok', 'PERSON', 2], ['Midas International Asset Management', 'ORGANIZATION', 2], ['Elliott', 'PERSON', 12], ['Robert Yi', 'PERSON', 1], ['Shin Jong-kyun', 'PERSON', 1], ['Shin', 'PERSON', 3], ['Franz-Hermann Hirlinger', 'PERSON', 1], ['Hirlinger', 'PERSON', 1], ['Sustinvest Inc.', 'ORGANIZATION', 3], ['Kim Sang-jo', 'PERSON', 1], ['Hansung University', 'ORGANIZATION', 4], ['Jay Y. describe', 'PERSON', 1], ['Chung', 'PERSON', 7], ['Abhey Lamba', 'PERSON', 1], ['Mizuho Securities', 'ORGANIZATION', 1], ['San Francisco', 'LOCATION', 2], ['Luca Maestri', 'PERSON', 1], ['Maestri', 'PERSON', 1], ['Toni Sacconaghi', 'PERSON', 1], ['Ford', 'ORGANIZATION', 4], ['New York', 'LOCATION', 8], ['Tim Cook', 'PERSON', 1], ['Cook', 'PERSON', 1], ['Jay Y. Lee', 'PERSON', 39], ['Park Ju-gun', 'PERSON', 6], ['Cheil', 'ORGANIZATION', 13], ['Sustinvest', 'PERSON', 1], ['National Pension Service', 'ORGANIZATION', 7], ['Glass Lewis & Co.', 'ORGANIZATION', 1], ['Institutional Shareholder Services Inc.', 'ORGANIZATION', 1], ['Glass Lewis', 'PERSON', 2], ['Lewis', 'PERSON', 2], ['Ko Young-yeel', 'PERSON', 2], ['Park', 'PERSON', 8], ['Lee Jae Yong', 'PERSON', 1], ['Ko', 'PERSON', 1], ['LG', 'ORGANIZATION', 6], ['Adam Minter', 'PERSON', 1], ['Timothy Lavin', 'PERSON', 1], ['D.J. Koh', 'PERSON', 7], ['Kim Young-woo', 'PERSON', 1], ['SK Securities Co.', 'ORGANIZATION', 1], ['G.S. Choi', 'PERSON', 1], ['Chang Sea-jin', 'PERSON', 2], ['National University of Singapore', 'ORGANIZATION', 2], ['Sony', 'ORGANIZATION', 5], ['Ridgefield Park', 'LOCATION', 1], ['Richard McCune', 'PERSON', 1], ['Waudby', 'PERSON', 1], ['U.S. District Court', 'ORGANIZATION', 1], ['New Jersey', 'LOCATION', 1], ['Newark', 'LOCATION', 1], ['Singapore', 'LOCATION', 1], ['BNP', 'ORGANIZATION', 3], ['FTSE Straits Times Real Estate Investment Trust', 'ORGANIZATION', 1], ['Jan Willem Vis', 'PERSON', 1], ['Bank of New York Mellon Corp.', 'ORGANIZATION', 1], ['Alan Richardson', 'PERSON', 1], ['Richardson', 'PERSON', 1], ['BNY Mellon', 'ORGANIZATION', 1], ['Schroders Plc', 'ORGANIZATION', 1], ['Ascendas Real Estate Investment Trust', 'ORGANIZATION', 1], ['Straits Times Index', 'ORGANIZATION', 1], ['Switzerland', 'LOCATION', 1], ['Italy', 'LOCATION', 1], ['Vikrant Pandey', 'PERSON', 1], ['UOB Kay Hian Pte.', 'ORGANIZATION', 1], ['Kar Tzen Chow', 'PERSON', 2], ['Affin Hwang Asset Management Bhd.', 'ORGANIZATION', 2], ['Affin Hwang', 'PERSON', 1], ['Mapletree Greater China Commercial Trust', 'ORGANIZATION', 1], ['Chow', 'PERSON', 1], ['Frasers Logistics', 'ORGANIZATION', 1], ['Mapletree Logistics', 'ORGANIZATION', 1], ['Croesus Retail Trust', 'ORGANIZATION', 1], ['Jason Pidcock', 'PERSON', 1], ['Jupiter Asset Management', 'ORGANIZATION', 1], ['Daiwa Capital Markets', 'ORGANIZATION', 1], ['David Lum', 'PERSON', 1], ['Daiwa', 'PERSON', 1], ['Lum', 'PERSON', 1], ['Hans Goetti', 'PERSON', 1], ['Middle East', 'LOCATION', 2], ['Banque Internationale', 'ORGANIZATION', 1], ['Luxembourg', 'LOCATION', 1], ['America', 'LOCATION', 4], ['Gartner', 'ORGANIZATION', 3], ['Tuong Nguyen', 'PERSON', 1], ['U.S. Transportation', 'ORGANIZATION', 2], ['American Airlines', 'ORGANIZATION', 2], ['Ross Feinstein', 'PERSON', 2], ['Hazardous Materials Safety Administration', 'ORGANIZATION', 2], ['Federal Aviation Administration', 'ORGANIZATION', 3], ['Anthony Foxx', 'PERSON', 1], ['DOT', 'ORGANIZATION', 1], ['FAA', 'ORGANIZATION', 3], ['Cho', 'PERSON', 1], ['Elliot Kaye', 'PERSON', 6], ['Kaye', 'PERSON', 3], ['Transportation Department', 'ORGANIZATION', 1], ['FedEx Corp.', 'ORGANIZATION', 2], ['United Parcel Service Inc.', 'ORGANIZATION', 2], ['Delta Air Lines Inc.', 'ORGANIZATION', 1], ['Southwest', 'ORGANIZATION', 10], ['Lori Crabtree', 'PERSON', 2], ['Qantas Airways Ltd.', 'ORGANIZATION', 1], ['Cathay Pacific Airways Ltd.', 'ORGANIZATION', 1], ['Alitalia', 'ORGANIZATION', 1], ['Hyundai', 'ORGANIZATION', 7], ['Bank of Korea', 'ORGANIZATION', 3], ['Lee Ju-yeol', 'PERSON', 3], ['Joo Hyung-hwan', 'PERSON', 1], ['Chung Chang-Won', 'PERSON', 1], ['Nomura Holdings Inc.', 'ORGANIZATION', 5], ['Yoo Jong-Woo', 'PERSON', 1], ['Korea Investment & Securities Co.', 'ORGANIZATION', 3], ['Yoo', 'PERSON', 1], ['Daishin Securities Co.', 'ORGANIZATION', 5], ['Alphabet Inc.', 'ORGANIZATION', 2], ['Google', 'ORGANIZATION', 12], ['John Elkann', 'PERSON', 1], ['TT International', 'ORGANIZATION', 1], ['HK -RRB- Ltd.', 'ORGANIZATION', 1], ['Skagen', 'LOCATION', 1], ['Duncan Robertson', 'PERSON', 1], ['Asia Pacific Equity Fund', 'ORGANIZATION', 1], ['Sri Lanka', 'LOCATION', 1], ['Knut Gezelius', 'PERSON', 1], ['Norway', 'LOCATION', 1], ['Samir Mehta', 'PERSON', 1], ['JO Hambro Capital Management', 'ORGANIZATION', 1], ['Chaiwon Lee', 'PERSON', 1], ['David Gaud', 'PERSON', 1], ['Edmond de Rothschild Asset Management', 'ORGANIZATION', 1], ['Srinivas Reddy', 'PERSON', 2], ['Center for Marketing Excellence', 'ORGANIZATION', 2], ['Singapore Management University', 'ORGANIZATION', 2], ['Reddy', 'PERSON', 1], ['Merck & Co.', 'ORGANIZATION', 1], ['Pinto', 'PERSON', 1], ['Indiana', 'LOCATION', 1], ['Takata Corp.', 'ORGANIZATION', 1], ['Peanut Corp.', 'ORGANIZATION', 1], ['Johnson & Johnson', 'ORGANIZATION', 1], ['Chicago', 'LOCATION', 2], ['Mattel Inc.', 'ORGANIZATION', 1], ['David Ramli', 'PERSON', 1], ['Yoolim Lee', 'PERSON', 1], ['Amperex Technology Ltd.', 'ORGANIZATION', 4], ['TDK', 'ORGANIZATION', 3], ['Vietnam', 'LOCATION', 2], ['Nguyen Mai', 'PERSON', 1], ['Association of Foreign Invested Enterprises', 'ORGANIZATION', 1], ['Nguyen Bich Lam', 'PERSON', 1], ['General Statistics Office', 'ORGANIZATION', 1], ['Alan Pham', 'PERSON', 1], ['Ho Chi Minh City', 'LOCATION', 2], ['VinaCapital Group Ltd.', 'ORGANIZATION', 1], ['Tran Tuan Anh', 'PERSON', 1], ['Pham', 'PERSON', 1], ['Philippines', 'LOCATION', 1], ['Mai', 'PERSON', 1], ['CPSC', 'ORGANIZATION', 4], ['Tim Baxter', 'PERSON', 1], ['Song Myung-sup', 'PERSON', 1], ['HI Investment & Securities Co.', 'ORGANIZATION', 5], ['UPS', 'ORGANIZATION', 1], ['U.K.', 'LOCATION', 2], ['Jim McCluskey', 'PERSON', 1], ['Verizon', 'ORGANIZATION', 3], ['U.S. Department of Transportation', 'ORGANIZATION', 1], ['Royal Mail', 'ORGANIZATION', 1], ['Parcelforce', 'ORGANIZATION', 1], ['UK Mail Group Plc', 'ORGANIZATION', 1], ['Deutsche Post', 'ORGANIZATION', 1], ['DHL', 'ORGANIZATION', 1], ['Germany', 'LOCATION', 5], ['Dirk Klasen', 'PERSON', 1], ['Bonn', 'LOCATION', 1], ['Greg Roh', 'PERSON', 6], ['HMC Investment Securities', 'ORGANIZATION', 6], ['Chung Chang Won', 'PERSON', 4], ['Shaun Rein', 'PERSON', 2], ['China Market Research Group', 'ORGANIZATION', 2], ['Chung Sun-sup', 'PERSON', 2], ['Roh', 'PERSON', 5], ['Huawei', 'ORGANIZATION', 3], ['Shinyoung', 'ORGANIZATION', 1], ['Martin Reynolds', 'PERSON', 1], ['Dell Inc.', 'ORGANIZATION', 2], ['Toshiba Corp.', 'ORGANIZATION', 1], ['Boeing Co.', 'ORGANIZATION', 2], ['Interbrand', 'ORGANIZATION', 2], ['Amazon', 'LOCATION', 1], ['Mercedes-Benz', 'ORGANIZATION', 2], ['Martin Roll', 'PERSON', 1], ['Ministry of Trade , Industry and Energy', 'ORGANIZATION', 1], ['Mark Newman', 'PERSON', 2], ['Sanford C. Bernstein', 'PERSON', 2], ['Yoo Jong Woo', 'PERSON', 1], ['Korean Investment & Securities Co.', 'ORGANIZATION', 1], ['Jonggak', 'LOCATION', 1], ['Shin Young-su', 'PERSON', 1], ['Kim Sung-min', 'PERSON', 1], ['Bernstein', 'PERSON', 1], ['Newman', 'PERSON', 1], ['Baker', 'PERSON', 1], ['Tim Culpan', 'PERSON', 8], ['Taipei', 'LOCATION', 7], ['Matthew Brooker', 'PERSON', 2], ['Lee Kun-Hee', 'PERSON', 4], ['Omnicom', 'ORGANIZATION', 1], ['Lenovo', 'ORGANIZATION', 1], ['Chinese', 'LOCATION', 2], ['Nokia', 'ORGANIZATION', 1], ['Leila Abboud', 'PERSON', 1], ['Paris', 'LOCATION', 2], ['James Boxell', 'PERSON', 1], ['Supreme Court', 'ORGANIZATION', 5], ['Washington', 'LOCATION', 7], ['Volkswagen', 'ORGANIZATION', 4], ['Samuel Alito', 'PERSON', 1], ['Anthony Kennedy', 'PERSON', 1], ['Facebook Inc.', 'ORGANIZATION', 3], ['EBay Inc.', 'ORGANIZATION', 2], ['Hewlett Packard Enterprises Co.', 'ORGANIZATION', 1], ['Seth Waxman', 'PERSON', 1], ['Kathleen Sullivan', 'PERSON', 1], ['Stephen Breyer', 'PERSON', 1], ['Royce', 'PERSON', 1], ['Sonia Sotomayor', 'PERSON', 3], ['Sotomayor', 'PERSON', 3], ['Waxman', 'PERSON', 1], ['Sullivan', 'PERSON', 1], ['U.S. Patent and Trademark Office', 'ORGANIZATION', 2], ['James Cordwell', 'PERSON', 1], ['LLP', 'ORGANIZATION', 2], ['AT&T', 'ORGANIZATION', 7], ['T-Mobile', 'ORGANIZATION', 3], ['Sprint Corp.', 'ORGANIZATION', 3], ['Telstra', 'ORGANIZATION', 5], ['IDC', 'ORGANIZATION', 3], ['Kulbinder Garcha', 'PERSON', 1], ['London', 'LOCATION', 1], ['Kim Sang Jo', 'PERSON', 1], ['Louisville', 'LOCATION', 6], ['Kentucky', 'LOCATION', 7], ['Korea Agency for Technology', 'ORGANIZATION', 1], ['Dan Baker', 'PERSON', 3], ['Morningstar Inc.', 'ORGANIZATION', 4], ['Saudi Arabia', 'LOCATION', 1], ['Angus Nicholson', 'PERSON', 1], ['Radiant Opto-Electronics Corp.', 'ORGANIZATION', 1], ['HannsTouch Solution Inc.', 'ORGANIZATION', 1], ['Alps Electric Co.', 'ORGANIZATION', 1], ['Japan Display Inc.', 'ORGANIZATION', 1], ['Murata Manufacturing Co.', 'ORGANIZATION', 1], ['Haruhiko Kuroda', 'PERSON', 1], ['Thailand', 'LOCATION', 2], ['OPEC', 'ORGANIZATION', 1], ['Toshihiko Matsuno', 'PERSON', 1], ['SMBC Friend Securities Co.', 'ORGANIZATION', 1], ['Republican', 'ORGANIZATION', 1], ['Donald Trump', 'PERSON', 2], ['Hillary Clinton', 'PERSON', 1], ['Yoo Jong-woo', 'PERSON', 2], ['General Administration', 'ORGANIZATION', 2], ['Alibaba Group Holding Ltd.', 'ORGANIZATION', 2], ['Viv Labs', 'PERSON', 1], ['Viv', 'PERSON', 2], ['Siri', 'PERSON', 2], ['Injong Rhee', 'PERSON', 1], ['Kirt McMaster', 'PERSON', 1], ['Cyanogen Inc.', 'ORGANIZATION', 1], ['McMaster', 'PERSON', 1], ['Hiroshi Lockheimer', 'PERSON', 1], ['Dag Kittlaus', 'PERSON', 2], ['Adam Cheyer', 'PERSON', 2], ['Chris Brigham', 'PERSON', 1], ['Jitendra Waral', 'PERSON', 1], ['Amazon', 'ORGANIZATION', 1], ['Silicon Valley', 'LOCATION', 1], ['Tim Tuttle', 'PERSON', 1], ['MindMeld Inc.', 'ORGANIZATION', 1], ['Farmington', 'LOCATION', 1], ['Minnesota', 'LOCATION', 1], ['Abby Zuis', 'PERSON', 1], ['Andrew Zuis', 'PERSON', 1], ['Abby', 'PERSON', 1], ['Zuis', 'PERSON', 1], ['Bryan Ma', 'PERSON', 1], ['Scott Wolfson', 'PERSON', 2], ['Texas', 'LOCATION', 1], ['Virginia', 'LOCATION', 1], ['Kelly Crummey', 'PERSON', 1], ['Fletcher Cook', 'PERSON', 3], ['Amperex', 'PERSON', 1], ['Song Eun-jeong', 'PERSON', 1], ['Dave Tovar', 'PERSON', 1], ['Blake Capital LLC', 'ORGANIZATION', 5], ['Potter Capital LLC', 'ORGANIZATION', 5], ['Kannon Shanmugam', 'PERSON', 1], ['HTC', 'ORGANIZATION', 1], ['Motorola Mobility', 'ORGANIZATION', 1], ['Paul Berghoff', 'PERSON', 1], ['McDonnell Boehnen Hulbert & Berghoff LLP', 'ORGANIZATION', 1], ['U.S. Court of Appeals', 'ORGANIZATION', 3], ['Kimberly Moore', 'PERSON', 1], ['Timothy Dyk', 'PERSON', 1], ['Dyk', 'PERSON', 1], ['Katrina Nicholas', 'PERSON', 4], ['Lee Seung-woo', 'PERSON', 1], ['IBK Securities Co.', 'ORGANIZATION', 1], ['Paul Elliott', 'PERSON', 1], ['Wei Jiang', 'PERSON', 1], ['Columbia Business School', 'ORGANIZATION', 1], ['Wall Street Journal', 'ORGANIZATION', 2], ['Jiang', 'PERSON', 1], ['Elliott Associates LP', 'ORGANIZATION', 2], ['C&T', 'ORGANIZATION', 6], ['Nguyen Thi Dung', 'PERSON', 1], ['Bac Ninh', 'LOCATION', 1], ['Ho Chi Minh', 'PERSON', 1], ['Nguyen Phuong Bac', 'PERSON', 1], ['Noi Bai International Airport', 'LOCATION', 1], ['Nguyen Duc Cao', 'PERSON', 1], ['Bac Ninh Industrial Zones Management Board', 'ORGANIZATION', 1], ['Thai Nguyen', 'LOCATION', 1], ['Scott Rozelle', 'PERSON', 1], ['Brian McCaig', 'PERSON', 1], ['Wilfrid Laurier University', 'ORGANIZATION', 1], ['Waterloo', 'LOCATION', 1], ['Ontario', 'LOCATION', 1], ['Canada', 'LOCATION', 1], ['McCaig', 'PERSON', 1], ['Le Thi Hoa', 'PERSON', 1], ['Bangladesh', 'LOCATION', 1], ['Indonesia', 'LOCATION', 1], ['Bac', 'PERSON', 1], ['Lan', 'PERSON', 1], ['Hana Financial Investment Co.', 'ORGANIZATION', 1], ['IT & Mobile Communications', 'ORGANIZATION', 1], ['Roko Kim', 'PERSON', 1], ['Pamela Gilbert', 'PERSON', 1], ['Gilbert', 'PERSON', 1], ['Cuneo Gilbert & LaDuca', 'ORGANIZATION', 1], ['Nancy Nord', 'PERSON', 1], ['Nord', 'PERSON', 1], ['Olsson Frank Weeda Terman Matz', 'PERSON', 1], ['Kevin Fletcher', 'PERSON', 1], ['Louisville Metro Arson Squad', 'ORGANIZATION', 1], ['Fletcher', 'PERSON', 1], ['Brian Green', 'PERSON', 1], ['Green', 'PERSON', 1], ['United Nations', 'ORGANIZATION', 2], ['Park Kang-ho', 'PERSON', 2], ['Crabtree', 'PERSON', 1], ['Natalie Chaudoin', 'PERSON', 1], ['Louisville Regional Airport Authority', 'ORGANIZATION', 1], ['Salvador Melendez', 'PERSON', 1], ['Louisville Fire Department', 'ORGANIZATION', 1], ['Melendez', 'PERSON', 1], ['Viv Labs Inc.', 'ORGANIZATION', 1], ['Rhee', 'PERSON', 1], ['Kittlaus', 'PERSON', 1], ['Lee Jay Yong', 'PERSON', 1], ['Dan Loeb', 'PERSON', 1], ['Third Point LLC', 'ORGANIZATION', 1], ['Seven & i Holdings Co.', 'ORGANIZATION', 2], ['Fanuc Corp.', 'ORGANIZATION', 1], ['Hess Corp.', 'ORGANIZATION', 1], ['EMC Corp.', 'ORGANIZATION', 1], ['Dell Technologies', 'ORGANIZATION', 1], ['Argentina', 'LOCATION', 1], ['CDK Global Inc.', 'ORGANIZATION', 1], ['Citrix Systems Inc.', 'ORGANIZATION', 1], ['Jesse Cohn', 'PERSON', 1], ['LogMeIn Inc.', 'ORGANIZATION', 1], ['Evergreen Coast Capital Corp.', 'ORGANIZATION', 1], ['Francisco Partners Management', 'ORGANIZATION', 1], ['Jay Y Lee', 'PERSON', 1], ['Jay Y', 'PERSON', 1], ['Qualcomm', 'ORGANIZATION', 2], ['Gillian Tan', 'PERSON', 1], ['Beth Williams', 'PERSON', 1], ['National Assembly', 'ORGANIZATION', 2], ['Kim Han-jung', 'PERSON', 1], ['Choi Soon-sil', 'PERSON', 15], ['Choi', 'PERSON', 15], ['NPS', 'ORGANIZATION', 7], ['Chu Jin-hyung', 'PERSON', 1], ['Hanwha', 'ORGANIZATION', 1], ['Chu', 'PERSON', 1], ['SK Group', 'ORGANIZATION', 6], ['Shin Dong-bin', 'PERSON', 2], ['Chey Tae-won', 'PERSON', 3], ['Chung Mong-koo', 'PERSON', 2], ['Billionaire Lee', 'PERSON', 1], ['Hanjin', 'ORGANIZATION', 2], ['Park Ju Gun', 'PERSON', 3], ['CEOSCORE', 'ORGANIZATION', 1], ['Chey', 'PERSON', 1], ['Lee In-won', 'PERSON', 1], ['Josh Rosenstock', 'PERSON', 1], ['Hewlett Packard Enterprise Co.', 'ORGANIZATION', 1], ['Matt Levy', 'PERSON', 1], ['Computer & Communications Industry Association', 'ORGANIZATION', 1], ['Levy', 'PERSON', 1], ['Obama', 'PERSON', 1], ['Rick McKenna', 'PERSON', 1], ['Foley & Lardner', 'ORGANIZATION', 1], ['Milwaukee', 'LOCATION', 1], ['Wisconsin', 'LOCATION', 1], ['McKenna', 'PERSON', 1], ['Harman International Industries Inc.', 'ORGANIZATION', 6], ['Navdy Inc.', 'ORGANIZATION', 1], ['Harman', 'PERSON', 5], ['Doug Simpson', 'PERSON', 1], ['Navdy', 'PERSON', 1], ['Simpson', 'PERSON', 1], ['Noah Feldman', 'PERSON', 1], ['Stacey Shick', 'PERSON', 1], ['Saenuri party', 'ORGANIZATION', 1], ['Choi Soon Sil', 'PERSON', 1], ['Kent Boydston', 'PERSON', 1], ['Peterson Institute for International Economics', 'ORGANIZATION', 1], ['Chun Doo-hwan', 'PERSON', 1], ['Feliz Navidad', 'PERSON', 1], ['Lotte Chairman Shin Dong-bin', 'PERSON', 1], ['Koo Bon-moo', 'PERSON', 1], ['Hanhwa Group', 'ORGANIZATION', 1], ['Kim Seung-youn', 'PERSON', 1], ['Cho Yang-ho', 'PERSON', 1], ['Sohn Kyung-shik', 'PERSON', 1], ['CJ Group', 'ORGANIZATION', 1], ['Huh Chang-soo', 'PERSON', 1], ['GS Group', 'ORGANIZATION', 1], ['Templeton Global Advisors', 'ORGANIZATION', 1], ['Norman Boersma', 'PERSON', 1], ['Templeton Growth Fund', 'ORGANIZATION', 1], ['Elliot Management Corp.', 'ORGANIZATION', 1], ['Boersma', 'PERSON', 1], ['Lees', 'PERSON', 1], ['Dong-Yang Kim', 'PERSON', 1], ['NH Investment & Securities Co.', 'ORGANIZATION', 1], ['Lee Sang-hoon', 'PERSON', 2], ['Blake Capital and Potter Capital', 'ORGANIZATION', 2], ['Lee Sang Hun', 'PERSON', 3], ['Cho Sung Ick', 'PERSON', 3], ['Korea Development Institute', 'ORGANIZATION', 3], ['Microsoft Corp.', 'ORGANIZATION', 1], ['Aberdeen', 'ORGANIZATION', 3], ['David Smith', 'PERSON', 3], ['Aberdeen', 'LOCATION', 1], ['Ben Franklins', 'PERSON', 1], ['Taiwan Semiconductor Manufacturing Co.', 'ORGANIZATION', 1], ['Foxconn', 'ORGANIZATION', 2], ['Daniel O\xe2\x80\x99Keefe', 'PERSON', 2], ['Artisan Partners', 'ORGANIZATION', 2], ['Smith', 'PERSON', 2], ['Visteon', 'ORGANIZATION', 2], ['Delphi', 'ORGANIZATION', 2], ['Mobileye NV', 'ORGANIZATION', 1], ['Morgan Stanley', 'ORGANIZATION', 1], ['Adam Jonas', 'PERSON', 1], ['Richard Hilgert', 'PERSON', 1], ['Mobileye', 'PERSON', 1], ['Standard & Poor', 'ORGANIZATION', 1], ['American Axle & Manufacturing Holdings', 'ORGANIZATION', 1], ['Adient Plc', 'ORGANIZATION', 1], ['Hilgert', 'PERSON', 1], ['Jim Fisher', 'PERSON', 1], ['Van Buren Township', 'LOCATION', 1], ['Hankook Tire Co.', 'ORGANIZATION', 1], ['Robert W. Baird & Co.', 'ORGANIZATION', 1], ['David Leiker', 'PERSON', 1], ['Jeffrey Owens', 'PERSON', 1], ['Owens', 'PERSON', 1], ['BMW AG', 'ORGANIZATION', 2], ['Ziv Aviram', 'PERSON', 1], ['Amnon Shashua', 'PERSON', 1], ['Robert Bosch GmbH', 'ORGANIZATION', 1], ['ZF Freidrichshafen AG', 'ORGANIZATION', 1], ['Continental AG', 'ORGANIZATION', 1], ['Panasonic Corp.', 'ORGANIZATION', 1], ['Jonas', 'PERSON', 1], ['Czech Republic', 'LOCATION', 1], ['Higher School of Economics', 'ORGANIZATION', 1], ['Mars Inc.', 'ORGANIZATION', 1], ['Magnus Benon', 'PERSON', 1], ['Ikea', 'ORGANIZATION', 1], ['Scandinavia', 'LOCATION', 1], ['Yaroslav Lissovolik', 'PERSON', 1], ['Eurasian Development Bank', 'ORGANIZATION', 1], ['Alexei Ulyukayev', 'PERSON', 1], ['Pakistan', 'LOCATION', 1], ['Tanzania', 'LOCATION', 1], ['World Bank', 'ORGANIZATION', 1], ['St. Petersburg', 'LOCATION', 1], ['Brazil', 'LOCATION', 1], ['Kazakhstan', 'LOCATION', 1], ['Economy Ministry', 'ORGANIZATION', 1], ['IHS Markit', 'ORGANIZATION', 1], ['Natalia Kostyukovich', 'PERSON', 1], ['Oleg Kouzmin', 'PERSON', 1], ['Moscow', 'LOCATION', 1], ['Young Sohn', 'PERSON', 2], ['Young', 'PERSON', 2], ['Stamford', 'LOCATION', 2], ['Wells Fargo', 'ORGANIZATION', 2], ['David Lim', 'PERSON', 2], ['Jim Hines', 'PERSON', 1], ['Hines', 'PERSON', 1], ['Toyota', 'ORGANIZATION', 2], ['Dinesh Paliwal', 'PERSON', 1], ['Paliwal', 'PERSON', 1], ['Jay Y. Lee Adding U.S.-based Harman', 'PERSON', 1], ['Elon Musk', 'ORGANIZATION', 1], ['Tesla Motors Inc.', 'ORGANIZATION', 1], ['Uber Technologies Inc.', 'ORGANIZATION', 1], ['BYD Co.', 'ORGANIZATION', 1], ['Sohn', 'PERSON', 1], ['McKinsey & Co.', 'ORGANIZATION', 1], ['Sidney Harman', 'PERSON', 1], ['Bernard Kardon', 'PERSON', 1], ['Infinity', 'ORGANIZATION', 1], ['Bang & Olufsen', 'ORGANIZATION', 1], ['Evercore', 'ORGANIZATION', 1], ['Lazard', 'PERSON', 1], ['Porsche', 'ORGANIZATION', 1], ['Bowers & Wilkins', 'ORGANIZATION', 1], ['Harman Kardon', 'PERSON', 1], ['New York Times', 'ORGANIZATION', 1], ['Washington Post', 'ORGANIZATION', 1], ['USA Today', 'ORGANIZATION', 1], ['Gregory Lee', 'PERSON', 1], ["Seoul Central District Prosecutors ' Office", 'ORGANIZATION', 2], ['Yonhap News', 'ORGANIZATION', 3], ['Chang', 'PERSON', 1], ['Corporate Strategy Office', 'ORGANIZATION', 1], ['Kim Sang-Jo', 'PERSON', 2], ['Solidarity for Economic Reform', 'ORGANIZATION', 1], ['SK Hynix Inc.', 'ORGANIZATION', 1], ['Korean Air Lines Co.', 'ORGANIZATION', 1], ['France', 'LOCATION', 1], ['Lamya Bouyirdane', 'PERSON', 1], ['The Associated Press', 'ORGANIZATION', 1], ['Bouyirdane', 'PERSON', 1], ['Pau', 'LOCATION', 1], ['William Stofega', 'PERSON', 1], ['SDI', 'ORGANIZATION', 1], ['Weibo', 'PERSON', 1], ['Tianjin', 'LOCATION', 1], ['Shin Yong-doo', 'PERSON', 1], ['Yuan Gao', 'PERSON', 1], ['Jungah Lee', 'PERSON', 1], ['Dan Doughty', 'PERSON', 1], ['Sandia National Laboratories', 'ORGANIZATION', 1], ['Institute of Electrical and Electronics Engineers Inc.', 'ORGANIZATION', 1], ['Doughty', 'PERSON', 1], ['Jim McGregor', 'PERSON', 1], ['Tirias Research LLC', 'ORGANIZATION', 1], ['McGregor', 'PERSON', 1], ['Barack Obama', 'PERSON', 1], ['Congress', 'ORGANIZATION', 2], ['Sharp Corp.', 'ORGANIZATION', 1], ['Sharp', 'PERSON', 1], ['Sakai', 'LOCATION', 1], ['Hon Hai Precision Industry Co.', 'ORGANIZATION', 1], ['Koh Dong-jin', 'PERSON', 1], ['UL LLC', 'ORGANIZATION', 1], ['Exponent Inc.', 'ORGANIZATION', 1], ['T\xc3\x9cV Rheinland Group', 'ORGANIZATION', 1], ['Koh', 'PERSON', 1], ['Barcelona', 'LOCATION', 1], ['Democratic Party of Korea', 'ORGANIZATION', 1], ['Moon Jae-in', 'PERSON', 1], ['Moon', 'PERSON', 6], ['Seoul Central District Court', 'ORGANIZATION', 2], ['Roh Moo-hyun', 'PERSON', 1], ['Kim Jong Il', 'PERSON', 1], ['Cho Eui-yeon', 'PERSON', 1], ['Kang Shin-up', 'PERSON', 2], ['Lee Kyu-chul', 'PERSON', 6], ['Choi Gee-sung', 'PERSON', 2], ['Troy Stangarone', 'PERSON', 3], ['Korea Economic Institute of America', 'ORGANIZATION', 3], ['Stangarone', 'PERSON', 3], ['Han Kyeong-jae', 'PERSON', 1], ['Moon Hyung-pyo', 'PERSON', 5], ['Lee Boo-jin', 'PERSON', 2], ['Lee Kyung-mook', 'PERSON', 1], ['Seoul National University', 'ORGANIZATION', 2], ['Graduate School of Business', 'ORGANIZATION', 1], ['Park Yong-jin', 'PERSON', 1], ['J.K. Shin', 'PERSON', 2], ['Yoon Boo-keun', 'PERSON', 2], ['Hotel Shilla Co.', 'ORGANIZATION', 2], ['Lee Seo-hyun', 'PERSON', 1], ['Heo', 'PERSON', 1], ['David Fickling', 'PERSON', 1], ['Sydney', 'LOCATION', 1], ['Graduate School of Public Administration', 'ORGANIZATION', 1], ['Chang Choong-ki', 'PERSON', 1], ['Korea Customs Service', 'ORGANIZATION', 2], ['Kim Kwie Sjamsudin', 'PERSON', 1], ['Yuanta Securities Indonesia', 'ORGANIZATION', 1], ['Jung Sung Han', 'PERSON', 1], ['Jung', 'PERSON', 1], ['LOT Vacuum Co.', 'ORGANIZATION', 1], ['Tera Semicon Co.', 'ORGANIZATION', 1], ['Soulbrain', 'LOCATION', 1], ['Inspectrum Tech Inc.', 'ORGANIZATION', 1], ['Posco', 'ORGANIZATION', 1], ['Lee Boo-Jin', 'PERSON', 1], ['Chung Yoo-ra', 'PERSON', 1], ['Incheon', 'LOCATION', 1]]

print len(total_list)
total_list.sort(key=lambda x:x[2], reverse=True)
k = total_list[0][2]

stats = []
for i in range(k):
    pruned = threshold(i+1, total_list)
    stats.append(len(pruned))

print stats

plt.plot(range(1, k+1), stats)
plt.title('Entity Number - Frequency Threshold')
plt.xlabel('Document Frequency')
plt.ylabel('Number of Entities')
plt.xlim(0, 20)
plt.grid(True)
plt.text(7,400,'The maximum frequency is 112', fontsize = 15)
plt.show()

# threshold test for person
person_list = [element for element in total_list if element[1] == 'PERSON']
person_list.sort(key=lambda x:x[2], reverse=True)
print person_list[0][2]
print(person_list[0:5])
per_name = []
for per in person_list[0:5]:
    per_name.append(per[0])
maxPerson = person_list[0][2]
person_entities = []
for seq in range(maxPerson):
    pruned = threshold(seq+1, person_list)
    person_entities.append(len(pruned))


# threshold test for organization
org_list = [element for element in total_list if element[1] == 'ORGANIZATION' and re.search('Samsung', element[0]) is None]
org_list.sort(key=lambda x:x[2], reverse=True)
print(org_list[0:5])
org_name = []
for org in org_list[0:5]:
    org_name.append(org[0])
maxOrg = org_list[0][2]
org_entities = []
for seq in range(maxOrg):
    pruned = threshold(seq+1, org_list)
    org_entities.append(len(pruned))

# threshold test for location
loc_list = [element for element in total_list if element[1] == 'LOCATION']
loc_list.sort(key=lambda x:x[2], reverse=True)
print(loc_list[0:5])
loc_name = []
for loc in loc_list[0:5]:
    loc_name.append(loc[0])
maxLoc = loc_list[0][2]
loc_entities = []
for seq in range(maxLoc):
    pruned = threshold(seq+1, loc_list)
    loc_entities.append(len(pruned))

# plt.plot(range(1, maxPerson+1), person_entities)
# plt.plot(range(1, maxOrg+1), org_entities)
# plt.plot(range(1, maxLoc+1), loc_entities)
# plt.title('PERSON, ORG, LOC - Frequency Threshold')
# plt.xlabel('Document Frequency')
# plt.ylabel('Number of Entities')
# plt.xlim(0, 10)
# plt.grid(True)
# plt.legend(['PERSON', 'ORGANIZATION', 'LOCATION'], loc='upper right')
# plt.text(3,220,'The maximum frequency is 39, 35, 64', fontsize = 15)
# plt.show()
#










path = '/Users/HENGJIE/Desktop/text repo/Bloomberg/samsung/pureBloomberg.txt'
with open(path, 'r') as f:
    lines = json.load(f)
    filtered_lines = [line for line in lines if line['title'].find('Samsung') >= 0]
    sub_lines = [line for line in filtered_lines if any(s in line['content'] for s in loc_name)]

text_path = '/Users/HENGJIE/Desktop/text repo/Bloomberg/samsung/org.txt'
g = open(text_path, 'a')
print len(sub_lines)
json.dump(sub_lines, g, indent=4)

#threshold plot for person, organization and location respectively
# plt.figure(1)
# plt.title('Threshold Plot')
# plt.subplot(311)
# plt.plot(range(2,maxPerson), person_entities)
# plt.xlabel('threshold')
# plt.ylabel('num_person')
#
# plt.subplot(312)
# plt.plot(range(2,maxOrg), org_entities, 'r')
# plt.xlabel('threshold')
# plt.ylabel('num_organization')
#
# plt.subplot(313)
# plt.plot(range(2,maxLoc), loc_entities, 'g')
# plt.xlabel('threshold')
# plt.ylabel('num_location')
#
# names = total_list[0:5]
# y = [name[2] for name in names]

# width = 0.8
# fig, ax1 = plt.subplots()
# ax1 = plt.subplot2grid((2,2),(0, 0), colspan = 2, rowspan = 2)
# plt.bar(range(0,5), y, width, alpha=1, color='g')
# ax1.set_ylabel('frequency')
# ax1.set_title('Null', fontsize=10, fontweight='bold')
# ax1.set_xticks([p + 1 * width for p in range(0, 5)])
# ax1.set_xticklabels([name[0] for name in names])
# plt.grid()
# plt.show()

# ax1 = plt.subplot2grid((3,3), (0,0), colspan=3)
# ax2 = plt.subplot2grid((3,3), (1,0), colspan=2)
# ax3 = plt.subplot2grid((3,3), (1, 2), rowspan=2)
# ax4 = plt.subplot2grid((3,3), (2, 0))
# ax5 = plt.subplot2grid((3,3), (2, 1))
# plt.show()

# width = 0.8
# fig, ax = plt.subplots()
# plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
# ax.set_ylabel('Number of tweets', fontsize=15)
# ax.set_title('Ranking: python vs. javascript vs. ruby (Relevant data)', fontsize=10, fontweight='bold')
# ax.set_xticks([p + 0.4 * width for p in x_pos])
# ax.set_xticklabels(langs)
# plt.grid()
#
# fig.savefig(fig_dir + "/img/figure1")


