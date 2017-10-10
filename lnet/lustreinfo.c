#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <lustre/lustreapi.h>
#include <lustre/lustre_user.h>
#include "lustreinfo.h"

#define MAX_OSTS 1024
#define LOV_EA_SIZE(lum, num) (sizeof(*lum) + num * sizeof(*lum->lmm_objects))
#define LOV_EA_MAX(lum) LOV_EA_SIZE(lum, MAX_OSTS)
 
/* Print out some LOV attributes. List our objects */
int get_file_info(char *path)
{
 
	struct lov_user_md *lump;
	int rc;
	int i;
     
	lump = malloc(LOV_EA_MAX(lump));
	if (lump == NULL) {
		return -1;
  }
 
  rc = llapi_file_get_stripe(path, lump);
        
  if (rc != 0) {
		fprintf(stderr, "get_stripe failed: %d (%s)\n",errno, strerror(errno));
		return -1;
  }
 
	printf("Lov magic %u\n", lump->lmm_magic);
	printf("Lov pattern %u\n", lump->lmm_pattern);
	//printf("Lov object id %llu\n", lump->lmm_object_id);
	//printf("Lov object group %llu\n", lump->lmm_object_gr);
	printf("Lov stripe size %u\n", lump->lmm_stripe_size);
	printf("Lov stripe count %hu\n", lump->lmm_stripe_count);
	printf("Lov stripe offset %u\n", lump->lmm_stripe_offset);
	for (i = 0; i < lump->lmm_stripe_count; i++) {
		printf("Object index %d %Lu %Lu Generation of OST index %d\n", lump->lmm_objects[i].l_ost_idx, lump->lmm_objects[i].l_ost_oi.oi.oi_id, lump->lmm_objects[i].l_ost_oi.oi.oi_seq, lump->lmm_objects[i].l_ost_gen);
		//printf("Object index %d Generation of OST index %d Objid %llu\n", lump->lmm_objects[i].l_ost_idx, lump->lmm_objects[i].l_ost_gen, lump->lmm_objects[i].l_object_id);
   }
 
	free(lump);
	return rc;
   
}

