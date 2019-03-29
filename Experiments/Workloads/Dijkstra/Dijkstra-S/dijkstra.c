/*
 * dijkstra.c
 *
 * Created: 2019-03-15 16:01:01
 *  Author: erikw_000
 */ 

#include<string.h>
#include<math.h>

#include "dijkstra.h"


int dijsktra(int cost[][N],int source,int target)
{
	int dist[N],prev[N],selected[N]={0},i,m,min,start,d,j;
	char path[N];
	for(i=1;i< N;i++)
	{
		dist[i] = IN;
		prev[i] = -1;
	}
	start = source;
	selected[start]=1;
	dist[start] = 0;
	while(selected[target] ==0)
	{
		min = IN;
		m = 0;
		for(i=1;i< N;i++)
		{
			d = dist[start] +cost[start][i];
			if(d< dist[i]&&selected[i]==0)
			{
				dist[i] = d;
				prev[i] = start;
			}
			if(min>dist[i] && selected[i]==0)
			{
				min = dist[i];
				m = i;
			}
		}
		start = m;
		selected[start] = 1;
	}
	start = target;
	j = 0;
	while(start != -1)
	{
		path[j++] = start+65;
		start = prev[start];
	}
	path[j]='\0';
	strrev(path);
	printf("%s", path);
	return dist[target];
}