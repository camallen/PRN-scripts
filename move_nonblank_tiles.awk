# awk -f move_nonblank_tiles.awk < nonblank_tile_list_before.txt | sh
#
{
  gsub("before", "after", $1)
  print("mv tiles_after_jpg/"$1 " nonblank/")


}
