import sqlite3
import json
import pandas as pd

def create_connection(db_file):
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
  return conn

def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)
    
def insert_into_weapons(conn, record):
  sql = """INSERT INTO WEAPONS(weapon_id, Name, Rarity, Class, Element, Type) VALUES(?,?,?,?,?,?)"""
  try:
    c = conn.cursor()
    c.execute(sql, record)
    conn.commit()
  except Error as e:
    print(e)  
    
def insert_into_perks(conn, record):
  sql = """INSERT INTO PERKS(weapon_id, Perk) VALUES(?,?)"""
  try:
    c = conn.cursor()
    c.execute(sql, record)
    conn.commit()
  except Error as e:
    print(e)  
    
def insert_into_stats(conn, record):
  sql = """INSERT INTO STATS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
  try:
    c = conn.cursor()
    c.execute(sql, record)
    conn.commit()
  except Error as e:
    print(e)  
    
def main():
  
  # create connection with database
  local_db_path = './destinyWeapons.db'
  conn = create_connection(local_db_path)
  
  createWeaponsTable = """
        CREATE TABLE IF NOT EXISTS WEAPONS (
          weapon_id INTEGER NOT NULL,
          Name VARCHAR(255) NOT NULL,
          Rarity VARCHAR(255) NOT NULL,
          Class VARCHAR(255) NOT NULL,
          Element VARCHAR(255) NOT NULL,
          Type VARCHAR(255) NOT NULL,

          PRIMARY KEY (weapon_id)
        );
        """
        
  createPerksTable = """
        CREATE TABLE IF NOT EXISTS PERKS (
          weapon_id INTEGER NOT NULL,
          Perk VARCHAR(55) NOT NULL,

          PRIMARY KEY (weapon_id, Perk),
          FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        );
        """
        
  createStatsTable = """
        CREATE TABLE IF NOT EXISTS STATS (
          weapon_id INTEGER NOT NULL,
          Impact INTEGER,
          Range INTEGER,
          Shield_Duration INTEGER,
          Handling INTEGER,
          Reload_Speed INTEGER,
          Aim_Assistance INTEGER,
          Inventory_Size INTEGER,
          Airborne_Effectiveness INTEGER,
          Rounds_Per_Min INTEGER,
          Charge_Time INTEGER,
          Magazine INTEGER,
          Stability INTEGER,
          Zoom INTEGER,
          Recoil INTEGER,
          Accuracy INTEGER,
          Draw_Time INTEGER,
          Velocity INTEGER,
          Blast_Radius INTEGER,
          Swing_Speed INTEGER,
          Guard_Efficiency INTEGER,
          Guard_Resistance INTEGER,
          Charge_Rate INTEGER,
          Ammo_Capacity INTEGER,

          PRIMARY KEY (weapon_id),
          FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        );
        """
  
  weapons_df = pd.read_json('weaponStats-Dec6.json', orient='record')
        
  if conn is not None:
    create_table(conn, createWeaponsTable)
    create_table(conn, createStatsTable)
    create_table(conn, createPerksTable)
    
    try:
      cur = conn.cursor()
      cur.execute("PRAGMA foreign_keys=ON;");
      conn.commit()
      print('Foreign keys are enabled')
    except Error as e:
      print(e)
    
    # insert weapons table data
    for index, row in weapons_df.iterrows():
      record = (row['weapon_id'], row['Name'], row['Rarity'], row['Class'], row['Element'], row['Type'])
      insert_into_weapons(conn, record)
    
    # insert weapon perk data
    for index, row in weapons_df.iterrows():
      id = row['weapon_id']
      for perk in [*set(row['Perks'])]: # use a set in case of duplicate perks so it doesn't crash
        record = (id, perk)
        insert_into_perks(conn, record)
        
    # insert weapon stat data
    for index, row in weapons_df.iterrows():
      record = (row['weapon_id'], row['Impact'], row['Range'], row['Shield Duration'], row['Handling'], row['Reload Speed'], row['Aim Assistance'], row['Inventory Size'], row['Airborne Effectiveness'], row['Rounds Per Minute'], row['Charge Time'], row['Magazine'], row['Stability'], row['Zoom'], row['Recoil'], row['Accuracy'], row['Draw Time'], row['Velocity'], row['Blast Radius'], row['Swing Speed'], row['Guard Efficiency'], row['Guard Resistance'], row['Charge Rate'], row['Ammo Capacity'])
      insert_into_stats(conn, record)
    
    print('success')
    
  else:
    print("Error! cannot create the database connection")

if __name__ == "__main__":
  main()