import os

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dorms = ['Balz-Dobie', 'East Lawn', 'Lile-Maupin', 'Bice House', 'Faulkner Apartments', 'Metcalf', 'Brown College', 'French House', 'Munford', 'Cauthen', 'Gibbons House', 'Shannon House', 'Copeley Bldg 829', 'Gooch', 'Shea House', 'Copeley Bldg 833', 'Gwathmey', 'Spanish House', 'Copeley Bldg 836', 'Hereford College (Runk)', 'Tuttle-Dunnington', 'Copeley Bldg 839', 'Kellogg', 'Watson-Webb', 'Dabney', 'Lambeth', 'Dillard', 'Lewis']

os.system('mkdir data')
for dorm in dorms:
    os.system('mkdir data/' + '"' + dorm + '"')
    for day in days:
        os.system('mkdir data/' + '"' + dorm + '"' + '/' + day)
