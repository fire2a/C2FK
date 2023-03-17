#ifndef FUELMODELKITRAL
#define FUELMODELKITRAL

#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <unordered_map>
#include <string>
#include <vector>

/*
*  Input, Fire, and output structures
*/

typedef struct
   { char fueltype[4];
     float ws, saz, cur, ps, cbh, ccf, cbd, elev , tmp, rh;
     int waz, nftype,FMC;
     float factor_cbd, factor_ccf, factor_ros10, factor_actv ;
	 bool cros, verbose;
   } inputs;


typedef struct
  { char fueltype[4] ;
    float fmc, cbh, fl ,h ;    // hros coef
    // Kitral:     l1 = 1.466, l2 = -0.01488
    // BehavePlus: l1 = 19.65, l2 = 0.00216
    // FARSITE:    l1 = 1.981, l2 = -0.02704
    // FBP System: l1 = 3.061, l2 = 0.02656
	int nftype; 
  } fuel_coefs;
  
  typedef struct
  { float fl, fh, a, b, c, rss, angle, byram,cfb,ros_active,se;
     char covertype;
	  int crown;
  } main_outs;

typedef struct
  { float ros, rss;
    double fi;
  } fire_struc;

  typedef struct
  { float lb, area, perm, pgr, lbt;
  } snd_outs;


 /*
		Functions
 */
// Initialize coefficients
void setup_const();

 // Calculate flank fire 
float flankfire_ros(float ros, float bros, float lb) ;

// Calculate rate of spread
float rate_of_spread(inputs *data, fuel_coefs *ptr, main_outs *at) ;

// Length-to-Breadth ratio
float l_to_b(float ws);

// BROS
float backfire_ros(main_outs *at, snd_outs *sec) ;

// Flame length [m])
float flame_length(inputs *data, main_outs *at);

// Angle of the flame w.r.t. horizontal surface (Putnam's)
float angleFL(inputs *data,  main_outs *at) ;

// Transformation from FL to FH using angle 
float flame_height(inputs* data,  main_outs *at);

//byram intensity
float byram_intensity(inputs* data, main_outs* at);

// Type of fire (Crown = 1, SROS = 0)
bool fire_type(inputs *data, main_outs* atr) ;
//Active crown
bool checkActive(inputs * data,main_outs* at);
// CROS adjustements
float final_rate_of_spreadFM10(main_outs* at) ;
float active_rate_of_spreadFM10(inputs* data,main_outs *at); //En KITRAL SE USA PL04
float crownfractionburn(inputs* data, main_outs* at);
bool checkActive(inputs * data,main_outs* at);

// Back fire with CROS 
float backfire_ros10(fire_struc *hptr, snd_outs *sec) ;

// Slope effect
float slope_effect(float elev_i, float elev_j, int cellsize);

// Main function to populate spread outputs based on inputs provided from main class
void calculate(inputs *data, inputs *head , int cellsize, fuel_coefs * ptr, main_outs *at, snd_outs *sec, fire_struc *hptr, fire_struc *fptr,fire_struc *bptr,bool & activeCrown);

void determine_destiny_metrics(inputs* data, fuel_coefs* ptr, main_outs* at);

#endif
