import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;

public class DBMS {
  public static void main(String[] args) {

    Scanner sc = new Scanner(System.in);
    Connection connection = null;

    try {
      // Create connection to db
      connection = DriverManager.getConnection("jdbc:sqlite:destiny.db");
      Statement statement = connection.createStatement();
      statement.setQueryTimeout(30);

      // Add tables
      createTables(statement);

    } catch (SQLException e) {
      System.err.println(e.getMessage());
    } finally {
      sc.close();
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