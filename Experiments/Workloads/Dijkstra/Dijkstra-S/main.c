#include <atmel_start.h>

/*
These values have been generated using the following python script:

import numpy as np
np.random.seed(314)
nodes = 128
connectedness = 0.5
int_max = 255
randints = np.random.randint(int_max/connectedness, size=nodes*nodes)
randints[randints > int_max] = 0
s = "{\n"
	for i in range(nodes):
	s += "\t{"
		for j in range(nodes):
		s += f"{randints[i*nodes+j]:3}, "
	s += "},\n"
s += "};"
print(s)
*/


//#define DEBUG_PRINT

#ifdef DEBUG_PRINT
#include <stdio.h>
#endif // DEBUG_PRINT

#define INFINITY 255
#define NUM_NODES 32


void dijkstra(uint8_t G[NUM_NODES][NUM_NODES], uint8_t startnode);

int main(void)
{
	int kj = 0;
	static uint8_t G[NUM_NODES][NUM_NODES] = {
        {  0,   0,   0,   0, 226,   0,   0,  71,  80,   0,   0,   0,   4,   0,   0,   0,   0, 111,   0,   0,  54,   0,   0,   0,   0,   0,   0,   0,   0,   0, 227,   0, },
        {  0,   0,   0,   0,   0,   0,   0,   0,   0, 137,   0,   0,   0,   0,   0,   0, 124,   0,   0,   0,   0,   0,  97, 250,   0,   0,   0,   0,   0,   0,   0, 112, },
        {  0,   0, 145,   0,   0,   0,   0,   3,   0,   0,   0,   0,   0,  42,   0,   0,   0,   0, 225,   0,   0,   0,   0,   0,   0,   0, 101,   0,   0,   0,   0,   0, },
        {  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 134,   0,   0,   0,   0, 158,  27,  90,  15,   0,   0, },
        {135,   0,   0,   0,   0,   0,   0, 142,   0,  57,   0,   0,   0, 112,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 222,   0,   0,   0,  27,   0, },
        {  0,   0,   0,   0,   0,   0,   0,  26,   0,   0,   0,   0, 111,   0,   0, 140,   0,   0,   0,  98,   0, 121,   0,   0,   0,   0,   0,   0,   0, 196,   0,   0, },
        {  0,   0,   0, 111,   0,  39,   0,   0,   0,  23,   0,   0,  92, 237,   0,   0,   0,   0,   0,   0,   0,   0,   5,   0,   0,   0,   0, 154,   0,   0,   0, 247, },
        {  0,   0,   0, 231,   0,   0,   0,   0,   0,   0,  89, 126,   0,   0,   0,   0,   0,   0,   0, 232,   0,   0,   0, 221,   0,   0,   0,   0,   0,   0,  78,   0, },
        {  0,   0, 110,   0,   0,   0,   0,   0,   0,   0, 135,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 253,  28,   0, 141,   0,   0,   0,   0,   0, },
        {221,   0,   0,  72,   0,   0,   0,   0,   0,   0,   0,   0, 188,   0, 214,   0, 228,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  29, 106, },
        { 62,   0, 150,   0,   0,   0,   0,   0,  96,  84,   0,  90,   0,   0,   0,   0,   0,   0, 127,   0,  86,   0,   0, 190,   0,   0,   0,   0,   0,  65,   0,   0, },
        {209,   0, 154,   0,   0,   0, 202,   0,   0, 175,   0,   0,   0,   0,   0,   0, 237, 158,   0,   0,   0,   0, 208,   0,   0,   0, 141,   0,   0,   0,   0,   0, },
        {  0,   0, 135, 109,   0,   0,  78,   0,   0,   0,   0,   0,   0,   0,   0, 153,   0,   0,   0,   0, 218,   0,   0, 103,   0,   0,   0,   0,   0,   0,   0, 209, },
        {  0,   0, 199,   0,   0,   0,   0,   0,   0,   0,   0,   0, 171,   0,   0,   0,   0,   0, 219,   0,   0,   0,   0,   0,   0, 101,   0,   0,  82, 161,   0,   0, },
        {  0,   0,  21,   0,   0,   0,   0, 130,   0,   0,   0,   0,  22,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   6,   0,   0,  13,  34,   0,   0, 195,  98, },
        {214,   0,  89,   0,   0,   0,   0,   0,   0,  78,   0, 251,   0,  41,   0,   0,   0,   0,   0,   0, 149,   0,   0,   0, 211,   0,   0,   0,   0,  22,   0,   0, },
        {  0,   0,   0,   0,  19,   0,   0,   0,   0, 234,   0,   0,   0,   0,   0,   0, 132,   0,   0,   0,   0,   0,  87,   0,   0,   0, 185,   0,   0,   0,   0,   0, },
        {  0,   2,   0,   0,   0,   0,   0,   0,   0,   0,  86,   0,   0, 168,   0,  74,   0,   0,   1,  40,   0,   0,   0, 103,   0,   0,   0,   0,   0,   0,   0,   0, },
        {  0,   0,  54,  23,  89,   0,  62,  34,   0,   0,   0,   0,  29,   0,   0,   0,   0,   0,   0,   0, 171,   0,   0,   0,   0,   0,   0,   0,   0,   0, 225,   0, },
        {  0,   0,   0,   0, 143,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 252,   0,   0,   0, 161,   0,   0,   0,   0,   0,   0,   0, },
        {  0,   0,   0,   0,   0,   0,   0,   0,  22,   0,   0, 112,  56,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 101, },
        {  0,   0, 230, 137,   0,   0,   0,   0,   0,   0,   0, 172,   0,   0,   0, 137,   0,   0, 186,   0, 213,   0,   0,   0, 117,  18,   0,   0,  14,   0,   0,   0, },
        {  0,   0,   0, 242,   0,   0,   0,   0, 206,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 243,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, },
        {  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 179,  53, 175, 154, 205,   0,   0,   0,   0,   0,   0, 207,   0,   0,   0,   0, },
        {  7,   0,  76,   0,   0,   0,  22,   0,   0,   0,   0,   0,   0,   0,   0, 219,   0,   0,   0,   0,   0, 115, 179,   0,   0,   0, 208,   0,   0,   0,   0,   0, },
        {250,   0,   0,   0,   0,   0,   0,   0,   0,   0, 135,   0,   0,   0,  29,   0,   0,   0,   0,   0,   0, 223,   0,   0,   0,   0,   1,   0,   0,  26,   0,   0, },
        {  0,   0,   0, 196, 235,   0,   0,   0, 159,   0,   0,   0,   0,   0, 113, 165,   0,   0, 158,   0,   0,  23,   0,   0,   0,   0,   0, 162,   0,   0,   0,   0, },
        {  0,   0,   0,   0,   0,   0,   0,   0,   0, 109,   0,   0,   0,  38,   0, 203,   0,   0,   0, 160,   0, 114,   0,  14,  20,   0,   0,   0,   0, 184,   0,   0, },
        {243,   0,   0,   0,   6,   0,   0,   0,   0,   0,  28,   0,   0,   0,  87,   0,   0,  93,   0,  36,   0,   0,   0,   0, 247,   0,   0, 214,   0,   0,   0,   0, },
        {  0,   0,   0,   0,   0,   0,   0,  92,   0,  88,   0,   0,   0,   0,  81,   0,   0, 169,   0,   0,   0,  25,   0,   0, 179,  87,   0,   0,   0,   0,   0,   7, },
        {  0,   0,   0,   0,   0,   0,   0,   0,  85,   0,   0,  27,  34,   0,   0,   0,   0,   0,   0,   3,   0,   0,   0,  43,   7,   0,  69,   0,   0,   0,   0,  25, },
        {  0,   0,   0,   0,   0, 181,  27,   0,   0, 155,   0,  88,   0,   0,   0,  48,   0,   0,   0, 125,   0,   0, 188,   0,   0,   0,  36,   0, 133,   0,   0,   0, },
    };

#ifdef DEBUG_PRINT
        for(uint8_t i=0;i<NUM_NODES;i++)
	    {
			for(uint8_t j=0;j<NUM_NODES;j++)
			{
				printf("%4d",G[i][j]);
			}
	        printf("\n");
	    }
#endif // DEBUG_PRINT

	uint8_t u = 0;
	dijkstra(G,u);

	return 0;
}

void dijkstra(uint8_t G[NUM_NODES][NUM_NODES], uint8_t startnode)
{

	uint8_t cost[NUM_NODES][NUM_NODES],distance[NUM_NODES];
#ifdef DEBUG_PRINT
	uint8_t pred[NUM_NODES];
#endif // DEBUG_PRINT
	uint8_t visited[NUM_NODES],count,mindistance,i,j;
	uint8_t nextnode = 0;

	//pred[] stores the predecessor of each node
	//count gives the number of nodes seen so far
	//create the cost matrix
	for(i=0;i<NUM_NODES;i++)
		for(j=0;j<NUM_NODES;j++)
			if(G[i][j]==0)
				cost[i][j]=INFINITY;
			else
				cost[i][j]=G[i][j];

	//initialize pred[],distance[] and visited[]
	for(i=0;i<NUM_NODES;i++)
	{
		distance[i]=cost[startnode][i];
#ifdef DEBUG_PRINT
		pred[i]=startnode;
#endif // DEBUG_PRINT
		visited[i]=0;
	}

	distance[startnode]=0;
	visited[startnode]=1;
	count=1;

	while(count<NUM_NODES-1)
	{
		mindistance=INFINITY;

		//nextnode gives the node at minimum distance
		for(i=0;i<NUM_NODES;i++)
			if(distance[i]<mindistance&&!visited[i])
			{
				mindistance=distance[i];
				nextnode=i;
			}

		//check if a better path exists through nextnode
		visited[nextnode]=1;
		for(i=0;i<NUM_NODES;i++)
			if(!visited[i])
				if(mindistance+cost[nextnode][i]<distance[i])
				{
					distance[i]=mindistance+cost[nextnode][i];
#ifdef DEBUG_PRINT
					pred[i]=nextnode;
#endif // DEBUG_PRINT
				}
				count++;
	}

#ifdef DEBUG_PRINT
		//print the path and distance of each node
		for(uint8_t i=0;i<NUM_NODES;i++)
			if(i!=startnode)
			{
				printf("\ndistance of node%d=%d",i,distance[i]);
				printf("\npath=%d",i);

				j=i;
				do
				{
					j=pred[j];
					printf("<-%d",j);
				}while(j!=startnode);
			}
#endif // DEBUG_PRINT

}
