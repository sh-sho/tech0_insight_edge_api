import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()
# set env
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
# SSL_CA = os.getenv('SSL_CA')
# Obtain connection string information from the portal

config = {
    'host':MYSQL_HOST,
    'user':MYSQL_USERNAME,
    'password':MYSQL_PASSWORD,
    'database':DATABASE_NAME
    # 'ssl_ca':SSL_CA
}
# Construct connection string

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()

# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS GenMission;")
cursor.execute("DROP TABLE IF EXISTS GenStory;")
cursor.execute("DROP TABLE IF EXISTS Child;")
cursor.execute("DROP TABLE IF EXISTS Characters;")
cursor.execute("DROP TABLE IF EXISTS Mission;")
cursor.execute("DROP TABLE IF EXISTS Map;")
cursor.execute("DROP TABLE IF EXISTS User;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute("CREATE TABLE User (UserID INT AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(255),Email VARCHAR(255),EncryptedPassword VARCHAR(255),SignupDate DATETIME, LastLogin DATETIME, PostCode VARCHAR(10),Address VARCHAR(255),LifeStyle VARCHAR(255));")
print("Finished creating User table.")
cursor.execute("CREATE TABLE Map (MapID INT AUTO_INCREMENT PRIMARY KEY, MapPlace VARCHAR(255));")
print("Finished creating Map table.")
cursor.execute("CREATE TABLE Mission (MissionID INT AUTO_INCREMENT PRIMARY KEY, MissionName VARCHAR(255), MissionModel VARCHAR(255));")
print("Finished creating Mission table.")
cursor.execute("CREATE TABLE Characters (CharacterID INT AUTO_INCREMENT PRIMARY KEY, CharacterName VARCHAR(255));")
print("Finished creating Characters table.")
cursor.execute("CREATE TABLE Child (ChildID INT AUTO_INCREMENT PRIMARY KEY, UserID INT, ChildName VARCHAR(255), ChildAge INT, ChildGender VARCHAR(10), ChildDetail TEXT, FOREIGN KEY (UserID) REFERENCES User(UserID));")
print("Finished creating Child table.")
cursor.execute("CREATE TABLE GenMission (GenMissionID INT AUTO_INCREMENT PRIMARY KEY, UserID INT, GenMissionRequest TEXT, GenMissionResponse TEXT, MissionID INT, MapID INT, ChildID INT, CharacterID INT, MissionTime DATETIME, Language VARCHAR(50),  \
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID), FOREIGN KEY (MapID) REFERENCES Map(MapID), FOREIGN KEY (ChildID) REFERENCES Child(ChildID), FOREIGN KEY (CharacterID) REFERENCES Characters(CharacterID), FOREIGN KEY (UserID) REFERENCES User(UserID));")
print("Finished creating GenMission table.")
cursor.execute("CREATE TABLE GenStory (GenStoryID INT AUTO_INCREMENT PRIMARY KEY, UserID INT, GenStoryRequest TEXT, GenStoryResponse TEXT, MapID INT, ChildID INT, CharacterID INT, Language VARCHAR(50),  \
    FOREIGN KEY (MapID) REFERENCES Map(MapID), FOREIGN KEY (ChildID) REFERENCES Child(ChildID), FOREIGN KEY (CharacterID) REFERENCES Characters(CharacterID), FOREIGN KEY (UserID) REFERENCES User(UserID));")
print("Finished creating GenMission table.")

# Insert some data into User table
cursor.execute("INSERT INTO User (Username, Email, EncryptedPassword, SignupDate, LastLogin, PostCode, Address, LifeStyle) VALUES\
    ('田中太郎', 'tanaka@example.com', 'hashed_password_123', '2023-01-01 12:00:00', '2023-01-02 15:30:00', '12345', '東京都港区', 'アクティブ'),\
    ('鈴木花子', 'suzuki@example.com', 'hashed_password_456', '2023-01-02 09:45:00', '2023-01-03 18:20:00', '54321', '大阪府大阪市', 'フィットネス愛好者'),\
    ('佐藤健太', 'sato@example.com', 'hashed_password_789', '2023-01-03 14:30:00', '2023-01-04 12:10:00', '67890', '福岡県福岡市', 'フーディー');")
print("Inserted",cursor.rowcount,"row(s) of data to User table.")

cursor.execute("INSERT INTO Map (MapPlace) VALUES ('品川'), ('渋谷');")
print("Inserted",cursor.rowcount,"row(s) of data to Map table.")

cursor.execute("INSERT INTO Mission (MissionName, MissionModel) VALUES ('Explore Ruins', 'ModelA'), ('Collect Artifacts', 'ModelB'), ('Rescue Team Members', 'ModelC'),('Navigate Maze', 'ModelA'),('Survival Challenge', 'ModelB');")
print("Inserted",cursor.rowcount,"row(s) of data to Mission table.")

cursor.execute("INSERT INTO Characters (CharacterName) VALUES ('ピカチュウ');")
print("Inserted",cursor.rowcount,"row(s) of data to Characters table.")

cursor.execute("INSERT INTO Child (UserID, ChildName, ChildAge, ChildGender, ChildDetail) VALUES \
    (1, 'ゆうき', 5, '男の子', 'おもちゃの車で遊ぶのが好きです。'),\
    (2, 'なおみ', 8, '女の子', '絵を描くのが好きで、絵具で色鮮やかな絵を描きます。'),\
    (3, 'しゅん', 6, '男の子', '動物に興味があり、特に犬や猫が好きです。');")
print("Inserted",cursor.rowcount,"row(s) of data to Child table.")

cursor.execute("INSERT INTO GenMission (UserID, GenMissionRequest, GenMissionResponse, MissionID, MapID, ChildID, CharacterID, MissionTime, Language) VALUES\
    (1, 'Explore the ancient ruins and find the hidden artifact.', 'Mission completed successfully.', 1, 2, 1, 1, '2023-01-10 08:30:00', 'English'),\
    (2, 'Rescue the team members trapped in the cave.', 'Team members rescued successfully.', 1, 1, 1, 1, '2023-01-15 12:45:00', 'Spanish'),\
    (2, 'Navigate through the maze and reach the destination.', 'Mission completed successfully.', 1, 2, 2, 1, '2023-01-20 15:20:00', 'French');")
print("Inserted",cursor.rowcount,"row(s) of data to GenMission table.")

cursor.execute("INSERT INTO GenStory (GenStoryRequest, GenStoryResponse, UserID, ChildID, MapID, CharacterID, Language) VALUES\
('Embark on a magical journey through the enchanted forest.', 'The magical creatures guide you to a hidden treasure.', 1, 1, 2, 1, 'English'),\
('Discover the secrets of the ancient castle.', 'You uncover a long-lost royal artifact.', 2, 2, 1, 1, 'Japanese'),\
('Sail across the vast ocean to a mysterious island.', 'You encounter friendly islanders who share their cultural traditions.', 2, 2, 1, 1, 'Spanish');")
print("Inserted",cursor.rowcount,"row(s) of data to GenStory table.")

# Commit
conn.commit()

# Select
cursor.execute("SELECT child.childname FROM user INNER JOIN child ON user.userid = child.userid WHERE user.username = '田中太郎' ;")
result = cursor.fetchall()
print(result)


# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")













