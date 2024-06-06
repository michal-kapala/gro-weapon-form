import os, sqlite3
from component import Component, WCMT
from dotenv import load_dotenv
from werkzeug.datastructures import ImmutableMultiDict

load_dotenv()

class DB:
  CONNECTION = sqlite3.connect(os.getenv("SQLITE_PATH").replace('\\', '\\\\'), check_same_thread=False)
  CUR = CONNECTION.cursor()

  def add_sku(self, name: str, oasis: int, price_rp: int, price_gc: int) -> int:
    """Returns the ID of a new SKU."""
    
    data = {
      "type": 0,
      "aStock": 0,
      "tStart": 0,
      "tExpired": 0,
      "IGCcost": price_rp,
      "GRcost": price_gc,
      "key": 0,
      "name": name,
      "oasisname": oasis
    }

    self.CUR.execute("""
                    INSERT INTO skus (type, aStock, tStart, tExpired, IGCcost, GRcost, key, name, oasisname)
                    VALUES (:type, :aStock, :tStart, :tExpired, :IGCcost, :GRcost, :key, :name, :oasisname)
                    """, data)
    id = self.CUR.execute("SELECT last_insert_rowid()").fetchone()[0]
    self.CUR.execute("""UPDATE skus SET iid=? WHERE id=?""", (id, id))
    return id

  def add_templ_item(self, name: str, oasis: int, weapon_class: str) -> int:
    """Returns the ID of a new template item."""
    match weapon_class:
      case "Assault rifle":
        oasis_desc = 70928
      case "Sniper rifle":
        oasis_desc = 70931
      case "Shotgun":
        oasis_desc = 70932
      case "SMG":
        oasis_desc = 70930
      case "LMG":
        oasis_desc = 70929
      case "Pistol":
        oasis_desc = 70933
      case "Grenade":
        # frag description
        oasis_desc = 73731

    data = {
      "type": 2,
      "name": name,
      "dtype": 0,
      "insideinventory": 1,
      "sellable": 1,
      "lootable": 1,
      "rewardable": 1,
      "unlockable": 1,
      "maxslot": 1,
      "gearscore": 0,
      "IGCvalue": 1.0,
      "oname": oasis,
      "odesc": oasis_desc
    }

    self.CUR.execute("""INSERT INTO templateitems 
      (type, name, dtype, insideinventory, sellable, lootable, rewardable, unlockable, maxslot, gearscore, IGCvalue, oname, odesc)
      VALUES (:type, :name, :dtype, :insideinventory, :sellable, :lootable, :rewardable, :unlockable, :maxslot, :gearscore, :IGCvalue, :oname, :odesc)""", data)
    id = self.CUR.execute("SELECT last_insert_rowid()").fetchone()[0]
    # -2 is situational
    self.CUR.execute("""UPDATE templateitems SET iid=? WHERE id=?""", (int(id) - 2, id))
    return int(id) - 2

  def add_sku_item(self, temp_item: int, sku: int, oasis: int) -> int:
    """Returns the ID of a new SKU item."""
    data = {
      "itemid": temp_item,
      "durability": 1,
      "durability2": 0,
      "oasisname": oasis,
      "IGCprice": 1,
      "GRprice": 1,
      "skuid": sku
    }

    self.CUR.execute("""INSERT INTO skuitems
                     (itemid, durability, durability2, oasisname, IGCprice, GRprice, skuid)
                     VALUES (:itemid, :durability, :durability2, :oasisname, :IGCprice, :GRprice, :skuid)""",
                     data)
    id = self.CUR.execute("SELECT last_insert_rowid()").fetchone()[0]
    return id
    
  def add_weapon(self, weapon_class: str, temp_item: int) -> int:
    """Returns the weapon's equippable class type."""
    match weapon_class:
      case "Assault rifle":
        class_type = 0
        eq_class_type = 1
      case "Sniper rifle":
        class_type = 1
        eq_class_type = 2
      case "Shotgun":
        class_type = 2
        eq_class_type = 4
      case "SMG":
        class_type = 3
        eq_class_type = 6
      case "LMG":
        class_type = 4
        eq_class_type = 3
      case "Pistol":
        class_type = 5
        eq_class_type = 7
      case "Grenade":
        class_type = 6
        eq_class_type = 5

    data = {
      "mapKey": temp_item,
      "classTypeID": class_type,
      "weaponType": class_type,
      "equippableClassType": eq_class_type,
      "flags": 0
    }

    self.CUR.execute("""INSERT INTO weapons (mapKey, classTypeID, weaponType, equippableClassType, flags)
                     VALUES (:mapKey, :classTypeID, :weaponType, :equippableClassType, :flags)""", data)
    id = self.CUR.execute("SELECT last_insert_rowid()").fetchone()[0]
    self.CUR.execute("UPDATE weapons SET weaponID=? WHERE id=?", (id, id))
    return eq_class_type
  
  def add_compat_bridge(self, map_key: int):
    """Adds a compatibility bridge entry."""
    data = {
      "key": map_key,
      "value": map_key
    }
    self.CUR.execute("""INSERT INTO weaponcompatbridge (key, value) VALUES (:key, :value)""", data)

  def add_unlock(self, temp_item: int, level: int):
    """Adds a level-based unlock for the weapon."""
    data = {
      "unlockItem": temp_item,
      "unlockType": 0,
      "classID1": 0,
      "level1": level,
      "classID2": 1,
      "level2": 0,
      "classID3": 2,
      "level3": 0,
      "achievID": 0,
      "achievWallID": 0,
      "fPoint1": 0,
      "fPoint2": 0,
      "fPoint3": 0,
      "fPoint4": 0,
      "fPoint5": 0
    }

    self.CUR.execute("""INSERT INTO unlocks
      (unlockItem, unlockType, classID1, level1, classID2, level2, classID3, level3, achievID, achievWallID, fPoint1, fPoint2, fPoint3, fPoint4, fPoint5)
      VALUES (:unlockItem, :unlockType, :classID1, :level1, :classID2, :level2, :classID3, :level3, :achievID, :achievWallID, :fPoint1, :fPoint2, :fPoint3, :fPoint4, :fPoint5)""", data)
    id = self.CUR.execute("SELECT last_insert_rowid()").fetchone()[0]
    self.CUR.execute("UPDATE unlocks SET iid=? WHERE id=?", (id, id))

  def add_components(self, form: ImmutableMultiDict[str, str], weapon_name: str) -> list[tuple]:
    """Creates component template items and components themselves."""
    comps = [
      { "type": WCMT.Body, "key": form["body"] },
      { "type": WCMT.ClassModifier, "key": form["class_modifier"] },
      { "type": WCMT.PrimaryAmmo, "key": form["primary_ammo"] },
      { "type": WCMT.UNUSED_AlternateAmmo, "key": form["unused_alternate_ammo"] },
      { "type": WCMT.Stock, "key": form["stock"] },
      { "type": WCMT.ForeGrip, "key": form["fore_grip"] },
      { "type": WCMT.Barrel, "key": form["barrel"] },
      { "type": WCMT.BarrelAttach, "key": form["barrel_attach"] },
      { "type": WCMT.Scope, "key": form["scope"] },
      { "type": WCMT.Clip, "key": form["clip"] },
      { "type": WCMT.GrenadeLauncher, "key": form["grenade_launcher"] },
      { "type": WCMT.Flashlight, "key": form["flashlight"] },
      { "type": WCMT.LaserPointer, "key": form["laser_pointer"] },
      { "type": WCMT.TopAmmoAttach, "key": form["top_ammo_attach"] },
      { "type": WCMT.StockAttach, "key": form["stock_attach"] },
      { "type": WCMT.FireModeFullAuto, "key": form["fire_mode_full_auto"] },
      { "type": WCMT.FireModeSemiAuto, "key": form["fire_mode_semi_auto"] },
      { "type": WCMT.FireModeBurst, "key": form["fire_mode_burst"] },
      { "type": WCMT.FireModeSingleShot, "key": form["fire_mode_single_shot"] },
      { "type": WCMT.FG_BottomAttach, "key": form["fg_bottom_attach"] },
      { "type": WCMT.ForeGripAndBarrel, "key": form["fore_grip_and_barrel"] },
      { "type": WCMT.Bipod, "key": form["bipod"] },
      { "type": WCMT.Melee, "key": form["melee"] },
      { "type": WCMT.Material, "key": form["material"] },
      { "type": WCMT.WeaponBoost, "key": form["weapon_boost"] }
    ]
    # copy as make_temp_items() mutates the list
    customizable = comps
    last_iid = self.CUR.execute("SELECT iid FROM templateitems WHERE id=(SELECT MAX(id) FROM templateitems)").fetchone()[0]
    temp_items = Component.make_temp_items(form, customizable, weapon_name, int(last_iid))
    self.CUR.executemany("""INSERT INTO templateitems
      (iid, type, name, dtype, insideinventory, sellable, lootable, rewardable, unlockable, maxslot, gearscore, IGCvalue, oname, odesc)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", temp_items)

    last_comp_id = self.CUR.execute("SELECT MAX(id) FROM components").fetchone()[0]
    # prevents the overlap with template item ids
    OFFSET = 10000
    gr5_comps, fgb_comp = Component.make_comps(comps, customizable, int(last_comp_id) + OFFSET)
    self.CUR.executemany("""INSERT INTO components (mapKey, iid, key, type, bonestructure, modifierlistid)
                            VALUES (?, ?, ?, ?, ?, ?)""", gr5_comps)

    # add FG & Barrel component
    if fgb_comp is not None:
      if "foregrip_mapkey" in fgb_comp and "barrel_mapkey" in fgb_comp:
        # child component refs
        list_id = self.CUR.execute(
          "SELECT MAX(listid) FROM skillmodifiers"
          ).fetchone()[0] + 1
        mod_id = self.CUR.execute(
          "SELECT MAX(id) FROM skillmodifiers"
          ).fetchone()[0]
        mods = [
          (list_id, mod_id + 1, 2, 105, 0, fgb_comp["foregrip_mapkey"]),
          (list_id, mod_id + 2, 2, 106, 0, fgb_comp["barrel_mapkey"])
        ]
        self.CUR.executemany("""INSERT INTO skillmodifiers (listid, modid, modtype, proptype, methodtype, methodval)
                                VALUES (?, ?, ?, ?, ?, ?)""", mods)
        # parent comp
        fgb = (fgb_comp["temp_item"], fgb_comp["temp_item"], fgb_comp["key"], fgb_comp["type"], 8, list_id)
        self.CUR.execute("""INSERT INTO components (mapKey, iid, key, type, bonestructure, modifierlistid)
                            VALUES (?, ?, ?, ?, ?, ?)""", fgb)
        gr5_comps.append(fgb)
      
    return gr5_comps

  def add_comp_list(self, comps: list[tuple], weapon_id: int):
    """Creates weapon's component map."""
    data = []
    for comp in comps:
      data.append((weapon_id, comp[0]))

    self.CUR.executemany("""INSERT INTO tempcomponentlists (key, value) VALUES (?,?)""", data)
