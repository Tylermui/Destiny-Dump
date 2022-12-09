from DBMS import create_connection
import inquirer
import re
import sys

WEAPONS_COLS = ['weapon_id', 'Name', 'Rarity', 'Class', 'Element', 'Type']
STATS_COLS = ['Impact', 'Range', 'Shield_Duration', 'Handling', 'Reload_Speed', 'Aim_Assistance', 'Inventory_Size', 'Airborne_Effectiveness', 'Rounds_Per_Min', 'Charge_Time', 'Magazine', 'Stability', 'Zoom', 'Recoil', 'Accuracy', 'Draw_Time', 'Velocity', 'Blast_Radius', 'Swing_Speed', 'Guard_Efficiency', 'Guard_Resistance', 'Charge_Rate', 'Ammo_Capacity']

def view_all_weapons(conn):
  try:
    cur = conn.cursor()
    cur.execute("SELECT Name FROM WEAPONS")
    rows = cur.fetchall()
    if len(rows) != 0:
      for row in rows: # row is a tuple
        print(row[0])
      print() # for buffer
    else:
      print('No weapons in database.')
  except Error as e:
    print(e)
    
def view_all_weapons_of_type(conn, w_type: str):
  try:
    cur = conn.cursor()
    cur.execute(f"SELECT Name FROM WEAPONS WHERE Type = '{w_type.title()}'")
    rows = cur.fetchall()
    if len(rows) != 0: # if no rows returned
      for row in rows: # row is a tuple
        print(row[0])
      print() # for buffer
    else:
      print(f'No weapons of type {w_type.title()}')
  except Error as e:
    print(e)

def view_all_types(conn):
  try:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Type FROM WEAPONS")
    rows = cur.fetchall()
    if len(rows) != 0:
      for row in rows:
        print(row[0])
      print() # for buffer
    else:
      print('No weapon types in database.')
  except Error as e:
    print(e)

def select_weapon(conn, weapon_name: str):
  # FIXME: error handling for if there is no weapon found
  try:
    cur = conn.cursor()
    # select basic weapon info
    cur.execute(f"SELECT * FROM WEAPONS WHERE Name = '{weapon_name.upper()}';")
    rows = cur.fetchall()
    print('WEAPON INFO:')
    if len(rows) != 0: # if there is data returned
      for row in rows:
        print() # buffer
        for i, value in enumerate(row):
          print('\t' + WEAPONS_COLS[i] + ': ' + str(value))
      print() # buffer
      
      print('STATS:')
      # select weapon stats
      cur.execute(f"SELECT * FROM STATS WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name.upper()}');")
      rows = cur.fetchall()
      for row in rows:
        print() # buffer
        for i, value in enumerate(row):
          # only print stats that have values, 0 is weapon_id
          if value is not None and i != 0: 
            # has to be i - 1 to ignore weapon_id column and still be aligned with rest of the columns
            print('\t' + STATS_COLS[i - 1] + ': ' + str(value))
      print() # buffer
      
      print('AVAILABLE PERKS:')
      cur.execute(f"SELECT Perk FROM PERKS WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name.upper()}');")
      rows = cur.fetchall()
      print() # buffer
      for row in rows:
        print('\t' + row[0]) # row is a tuple of selected columns
      print() # buffer
    
    else:
      print(f'\n{weapon_name.upper()} not in database.\n')
    
  except Error as e:
    print(e)

def delete_weapon(conn, weapon_name: str):
  try:
    cur = conn.cursor()
    cur.execute(f"DELETE FROM WEAPONS WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name.upper()}');")
    # documentation: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.rowcount
    if cur.rowcount < 1: 
      # error
      print(f'Unable to delete {weapon_name.upper()} from database.')
    else:
      # success
      conn.commit()
      print(f'Successfully deleted {weapon_name.upper()} from database!')
  except Error as e:
    print(e)

def insert_weapon(conn):
  w_answers = {}
  for q in WEAPONS_COLS:
    if q == 'weapon_id':
      answer = input(q + ' (INTEGER): ')
    else:
      answer = input(q + ' (VARCHAR):')
    if q == 'Name':
      w_answers[q] = answer.upper()
    else:
      w_answers[q] = answer.capitalize()
    
  s_answers = {}
  for q in STATS_COLS:
    answer = input(q + ' (INTEGER): ')
    s_answers[q] = answer
    
  perks = input('Enter a list of perks separated by comma: ').split(', ')
  
  weapon_id = w_answers['weapon_id']
  
  try:
    cur = conn.cursor()
    cur.execute("INSERT INTO WEAPONS(weapon_id, Name, Rarity, Class, Element, Type) VALUES(?,?,?,?,?,?)", list(w_answers.values()))
    if cur.rowcount < 1:
      # error
      print(f"Unable to add {w_answers['Name']} to WEAPONS table")
    else:
      # continue
      conn.commit()
      stats = [weapon_id] + list(s_answers.values())
      print(stats)
      cur.execute("INSERT INTO STATS VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", stats)
      if cur.rowcount < 1:
        # error
        print(f"Unable to add {w_answers['Name']} to STATS table")
      else:
        # continue
        conn.commit()
        # loop through perks and add
        for perk in perks:
          cur.execute("INSERT INTO PERKS(weapon_id, Perk) VALUES(?,?)", [weapon_id, perk])
          if cur.rowcount < 1:
            # error
            print(f"Unable to add {w_answers['Name']} to PERKS table")
            break
          else:
            conn.commit()
            continue
        print(f"Successfully added {w_answers['Name']} to database!")
  except Error as e:
    print(e)

def update_weapon(conn, weapon_name):
  questions = [
    inquirer.List('updateWeaponChoice', message=f'Select which table to update for {weapon_name}', choices=['WEAPONS', 'STATS', 'PERKS'])
  ]
  answers = inquirer.prompt(questions)
  if answers['updateWeaponChoice'] == 'WEAPONS':
    # update from weapons table
    column_to_update = input('Which column do you wish to update? ' + ' '.join(WEAPONS_COLS) + ': ')
    try:
      cur = conn.cursor()
      # can be numeric though
      if column_to_update == 'weapon_id':
        new_value = input(f'New value for {column_to_update} (INTEGER): ')
        cur.execute(f"UPDATE WEAPONS SET {column_to_update} = {int(new_value)} WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}');")
        if cur.rowcount < 1:
          print(f"\nUnable to update {column_to_update} = {new_value} for {weapon_name} in table WEAPONS.")
        else:
          print(f"\nSuccessfully updated {column_to_update} = {new_value} for {weapon_name} in table WEAPONS!\n")
          conn.commit()
      else:
        new_value = input(f'New value for {column_to_update} (VARCHAR): ')
        cur.execute(f"UPDATE WEAPONS SET {column_to_update} = '{str(new_value)} WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}');'")
        if cur.rowcount < 1:
          print(f"\nUnable to update {column_to_update} = {new_value} for {weapon_name} in table WEAPONS.\n")
        else:
          print(f"\nSuccessfully updated {column_to_update} = {new_value} for {weapon_name} in table WEAPONS!\n")
          conn.commit()
    except Error as e:
      print(e)
  elif answers['updateWeaponChoice'] == 'STATS':
    # update from stats table
    column_to_update = input('Which column do you wish to update? ' + ' '.join(STATS_COLS) + ': ')
    new_value = input(f'New value for {column_to_update} (INTEGER): ')
    try:
      cur = conn.cursor()
      # can be numeric though
      cur.execute(f"UPDATE STATS SET {column_to_update} = {int(new_value)} WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}');")
      if cur.rowcount < 1:
        print(f"\nUnable to update {column_to_update} = {new_value} for {weapon_name} in table STATS.\n")
      else:
        print(f"\nSuccessfully updated {column_to_update} = {new_value} for {weapon_name} in table STATS!\n")
        conn.commit()
    except Error as e:
      print(e)
  elif answers['updateWeaponChoice'] == 'PERKS':
    # update from perks table
    # query and display all perks
    try:
      cur = conn.cursor()
      cur.execute(f"SELECT * FROM PERKS WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}');")
      rows = cur.fetchall()
      if len(rows) != 0:
        for row in rows:
          print(row[1]) # row is tuple of weapon_id and perk name
        # update desired perk, if updated value is blank, delete the perk
        perk_to_update = input('\nWhat is the name of the perk you wish to update? ').capitalize()
        new_value = input(f'\nNew value for {perk_to_update}: ')
        if len(new_value) != 0:
          # update value
          cur.execute(f"UPDATE PERKS SET PERK = {new_value} WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}') AND Perk = '{perk_to_update}';")
          if cur.rowcount < 1:
            # error
            print(f"\nUnable to update Perk = {new_value} for {weapon_name} in table PERKS.\n")
          else:
            # success
            print(f"\nSuccessfully updated Perk = {new_value} for {weapon_name} in table PERKS!\n")
            conn.commit()
        else:
          # delete the perk
          cur.execute(f"DELETE FROM PERKS WHERE weapon_id IN (SELECT weapon_id FROM WEAPONS WHERE Name = '{weapon_name}') AND Perk = '{perk_to_update}';")
          if cur.rowcount < 1:
            # error
            print(f"\nUnable to delete Perk for {weapon_name} in table PERKS.\n")
          else:
            # success
            print(f"\nSuccessfully deleted Perk for {weapon_name} in table PERKS!\n")
            conn.commit()
      else:
        print(f'No perks found for {weapon_name}')
    except Error as e:
      print(e)
    
def restartOption():
    questions = [
        inquirer.List(
            "restartChoice",
            message="Would you like to query more?",
            choices=["Make another choice", "Exit the program"],
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers["restartChoice"] == "Make another choice":
        menu()
    elif answers["restartChoice"] == "Exit the program":
        sys.exit("Goodbye! Disconnecting from database...")

def menu():
  questions = [
      inquirer.List('initialChoice', message="Welcome to Destiny Dump! Select from one of the options below", choices=['Select Weapon', 'Update Weapon', 'Delete Weapon', 'Insert Weapon', 'View All Weapons', 'View All Weapon Types', 'View All Weapons of Specific Type'])
    ]
  answers = inquirer.prompt(questions)
  
  if answers['initialChoice'] == 'Select Weapon':
    # shows weapon name, stats, and available perks
    weapon_name = input('Enter the name of the weapon you wish to view: ')
    select_weapon(conn, weapon_name)
    restartOption()
  elif answers['initialChoice'] == 'Update Weapon':
    # update any aspect of a weapon
    weapon_name = input('Which weapon would you like to update? (Enter weapon name): ').upper()
    update_weapon(conn, weapon_name)
    restartOption()
  elif answers['initialChoice'] == 'Delete Weapon':
    # delete any weapon
    weapon_name = input('What is the name of the weapon you wish to delete? ')
    delete_weapon(conn, weapon_name)
    restartOption()
  elif answers['initialChoice'] == 'Insert Weapon':
    # insert any weapon
    insert_weapon(conn)
    restartOption()
  elif answers['initialChoice'] == 'View All Weapons':
    # displays all weapons
    view_all_weapons(conn)
    restartOption()
  elif answers['initialChoice'] == 'View All Weapon Types':
    # displays all the weapon types that are in the database
    view_all_types(conn)
    restartOption()
  elif answers['initialChoice'] == 'View All Weapons of Specific Type':
    # displays all the weapon types that are in the database
    w_type = input('What type of weapon do you wish to view? ')
    view_all_weapons_of_type(conn, w_type)
    restartOption()

if __name__ == '__main__':
  
  conn = create_connection('./destinyWeapons.db')
  
  if conn is not None:
    menu()
    conn.close()
  else:
    print("Error! cannot create the database connection")
