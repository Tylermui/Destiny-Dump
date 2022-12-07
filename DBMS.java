import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;
import com.opencsv.CSVReader;
import java.util.*;

public class DBMS {
  public static void main(String[] args) throws Exception {

    Scanner sc = new Scanner(System.in);
    FileReader fileReader = new FileReader("./weaponStatsWithPerks.csv");
    CSVReader csvReader = new CSVReader(fileReader);
    Connection connection = null;

    try {
      // Create connection to db
      connection = DriverManager.getConnection("jdbc:sqlite:destiny.db");
      Statement statement = connection.createStatement();
      statement.setQueryTimeout(30);

      // Add tables
      createTables(statement);
      String[] nextLine;
      csvReader.readNext();

      int weapon_id = 0; // FIXME: change this to be per row
      while ((nextLine = csvReader.readNext()) != null) { // reading and setting WEAPONS table
        String Name = nextLine[0];
        String Rarity = nextLine[1];
        String Class = nextLine[2];
        String Element = nextLine[3];
        String Type = nextLine[4];
        statement.executeUpdate("insert into WEAPONS values(" + weapon_id + ", '" + Name + "','" + Rarity + "','"
            + Class + "','" + Element + "','" + Type + "')");

        weapon_id++;
      }

      ResultSet rs = statement.executeQuery("select * from WEAPONS");
      while (rs.next()) // read the result set
      {
        System.out.println("WeaponID = " + rs.getInt("weapon_id"));
        System.out.println("Name = " + rs.getString("Name"));
        System.out.println("Rarity = " + rs.getString("Rarity"));
        System.out.println("Class = " + rs.getString("Class"));
        System.out.println("Element = " + rs.getString("Element"));
        System.out.println("Type = " + rs.getString("Type"));
      }
    } catch (SQLException e) {
      System.err.println(e.getMessage());
    } finally {
      sc.close();
      csvReader.close();
    }
  }

  public static void createTables(Statement statement) {
    String createWeaponsTable = """
        CREATE TABLE IF NOT EXISTS WEAPONS (
          weapon_id INTEGER NOT NULL,
          Name VARCHAR(100) NOT NULL,
          Rarity VARCHAR(20) NOT NULL,
          Class VARCHAR(7) NOT NULL,
          Element VARCHAR(15) NOT NULL,
          Type VARCHAR(30) NOT NULL,

          PRIMARY KEY (weapon_id)
        );
        """;

    String createPerksTable = """
        CREATE TABLE IF NOT EXISTS PERKS (
          weapon_id INTEGER NOT NULL,
          Perk VARCHAR(55) NOT NULL,

          PRIMARY KEY (weapon_id, Perk),
          FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        );
        """;

    String createStatsTable = """
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
        )
        """;

    try {
      statement.executeUpdate(createWeaponsTable);
      statement.executeUpdate(createPerksTable);
      statement.executeUpdate(createStatsTable);
      // Needed for foreign key updating
      statement.executeUpdate("PRAGMA foreign_keys=ON;");
    } catch (SQLException e) {
      System.err.println(e.getMessage());
    }

  }
}