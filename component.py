from enum import IntEnum
from werkzeug.datastructures import ImmutableMultiDict

class WCMT(IntEnum):
  """Weapon component (module?) types."""
  Body = 0
  ClassModifier = 1
  PrimaryAmmo = 2
  UNUSED_AlternateAmmo = 3
  Stock = 4
  ForeGrip = 5
  Barrel = 6
  BarrelAttach = 7
  Scope = 8
  Clip = 9
  GrenadeLauncher = 10
  Flashlight = 11
  LaserPointer = 12
  TopAmmoAttach = 13
  StockAttach = 14
  FireModeFullAuto = 15
  FireModeSemiAuto = 16
  FireModeBurst = 17
  FireModeSingleShot = 18
  FG_BottomAttach = 19
  ForeGripAndBarrel = 20
  Bipod = 21
  Melee = 22
  Material = 23
  WeaponBoost = 24

class Component:
  CUSTOM_COMPS = [
      WCMT.Stock,
      WCMT.BarrelAttach,
      WCMT.Scope,
      WCMT.Clip,
      WCMT.GrenadeLauncher,
      WCMT.Flashlight,
      WCMT.LaserPointer,
      WCMT.FG_BottomAttach,
      WCMT.ForeGripAndBarrel,
      WCMT.Bipod,
      WCMT.WeaponBoost
    ]
  
  def filter_customizable(comps: list[dict]) -> list[dict]:
    return [c for c in comps if c["key"] != "" and c["type"] in Component.CUSTOM_COMPS]

  def make_temp_items(form: ImmutableMultiDict[str, str], comps: list[dict], weapon_name: str, last_iid: int) -> list[tuple]:
    """Creates data for component template items."""
    # create template items only for the customizable components
    # see `GR5_Component::GetAttachableCompType` (0x10121A30) in AI.dll
    comps = Component.filter_customizable(comps)
    temp_items = []
    comp_name = ""
    oasis = 0
    # customizable components (see `GR5_Component::FillStats`` in AI.dll)
    for comp in comps:
      match comp["type"]:
        case WCMT.Stock:
          comp_name = "Fixed Stock"
          oasis = 70878
        case WCMT.ForeGrip:
          comp_name = "ForeGrip"
          oasis = 71816
        case WCMT.Barrel:
          comp_name = "Mid Barrel"
          oasis = 70876
        case WCMT.BarrelAttach:
          comp_name = "Muzzle Brake"
          oasis = 70883
        case WCMT.Scope:
          comp_name = "Scope"
          oasis = 70898
        case WCMT.Clip:
          comp_name = "Basic Clip"
          oasis = 70870
        case WCMT.GrenadeLauncher:
          comp_name = "Grenade Launcher"
          oasis = 70887
        case WCMT.Flashlight:
          comp_name = "Flashlight"
          oasis = 70890
        case WCMT.LaserPointer:
          comp_name = "Laser Pointer"
          oasis = 70889
        case WCMT.FG_BottomAttach:
          comp_name = "Bottom Attach"
          oasis = 71825
        case WCMT.ForeGripAndBarrel:
          comp_name = "Mid Barrel"
          oasis = 70876
        case WCMT.Bipod:
          comp_name = "Bipod"
          oasis = 70885
        case WCMT.WeaponBoost:
          comp_name = "Special Ammo"
          oasis = 73830

      # update id
      last_iid = last_iid + 1
      comp["temp_item"] = last_iid
      temp_items.append((last_iid, 4, f'{weapon_name} {comp_name}', 0, 1, 1, 0, 0, 1, 1, 0, 1.0, oasis, oasis))

    return temp_items

  def parse_hex(hex: str) -> int:
    """Parses a hex key into integer"""
    try:
      return int(hex, 16)
    except:
      return 0
    
  def make_comps(comps: list[dict], customizable_comps: list[dict], last_comp_id: int) -> tuple[list[tuple], dict]:
    """Creates `GR5_Component` data."""
    comps = [c for c in comps if c["key"] != ""]
    for comp in comps:
      comp["key"] = Component.parse_hex(comp["key"])

    # customizable component map keys/ids
    customizable_comps = Component.filter_customizable(customizable_comps)
    for cc in customizable_comps:
      for comp in comps:
        if cc["type"] == comp["type"]:
          comp["temp_item"] = cc["temp_item"]
          break

    # non-customizable component map keys/ids
    for comp in comps:
      last_comp_id = last_comp_id + 1
      if "temp_item" not in comp:
        comp["temp_item"] = last_comp_id

    foregrip_barrel_comp = None
    foregrip_mapkey = None
    barrel_mapkey = None
    data: list[tuple] = []
    bone = 255
    mod_list_id = 2
    for comp in comps:
      if comp["type"] == WCMT.ForeGripAndBarrel:
        foregrip_barrel_comp = comp
        continue
      elif comp["type"] == WCMT.ForeGrip:
        foregrip_mapkey = comp["temp_item"]
      elif comp["type"] == WCMT.Barrel:
        barrel_mapkey = comp["temp_item"]
      data.append((
        comp["temp_item"],
        comp["temp_item"],
        comp["key"],
        comp["type"],
        bone,
        mod_list_id
      )) 
    
    if foregrip_mapkey is not None:
      foregrip_barrel_comp["foregrip_mapkey"] = foregrip_mapkey
    if barrel_mapkey is not None:
      foregrip_barrel_comp["barrel_mapkey"] = barrel_mapkey

    return data, foregrip_barrel_comp
  