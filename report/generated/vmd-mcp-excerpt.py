    weight = "weight mass" if mass_weighted else ""
    tcl = f"""
{_load_block(structure, trajectory)}
set sel [atomselect $mol "{_tcl_quote(selection)}"]
set n [molinfo $mol get numframes]
for {{set i 0}} {{$i < $n}} {{incr i}} {{
  $sel frame $i
  puts "{MARKER} frame=$i rgyr=[measure rgyr $sel {weight}]"
}}
quit
"""
    res = _run_tcl(tcl)
    series = [
        {"frame": int(m["frame"]), "rgyr": float(m["rgyr"])}
        for m in res.get("markers", [])
        if "rgyr" in m
    ]
