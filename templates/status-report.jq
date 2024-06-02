{
  counts: (group_by(.productType) | map({(.[0].productType): group_by(.status) | map({(.[0].status): length}) | add}) | add),
  offlineDevices: map(select(.status == "offline").name)
}