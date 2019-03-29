#include <atmel_start.h>


#include "dijkstra.h"

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();

	int cost[N][N],i,j,w,ch,co;
	int source, target,x,y;
	printf("\t The Shortest Path Algorithm ( DIJKSTRA'S ALGORITHM in C \n\n");
	for(i=1;i< N;i++)
	for(j=1;j< N;j++)
	cost[i][j] = IN;
	for(x=1;x< N;x++)
	{
		for(y=x+1;y< N;y++)
		{
			printf("Enter the weight of the path between nodes %d and %d: ",x,y);
			scanf("%d",&w);
			cost [x][y] = cost[y][x] = w;
		}
		printf("\n");
	}
	printf("\nEnter the source:");
	scanf("%d", &source);
	printf("\nEnter the target");
	scanf("%d", &target);
	co = dijsktra(cost,source,target);
	printf("\nThe Shortest Path: %d",co);
}
