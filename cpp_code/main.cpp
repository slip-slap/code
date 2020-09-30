#include <iostream>
int main()
{
	int* test_arry ;
	test_arry= new int[20];
	std::cout<<"the 25th element: "<<test_arry[25000000]<<std::endl;
}


/*

#include<iostream>
#include <vector>
#include <queue>
#define I 32768


std::vector<int> minimum_cost_spanning_tree(float graph[4][4],int node_number)
{
	// initial state
	float minimum_edge = 10000;	
	std::vector<int> tree;
	std::vector<int> potiential_node(node_number);
	for(int i=0;i<potiential_node.size();i++)
	{
		potiential_node[i]=I;
	}
	int edge_node_1;
	int edge_node_2;
	for(int i=0;i<4;i++)
	{
		for(int j=i;j<4;j++)
		{
			if(minimum_edge>graph[i][j])
			{
				minimum_edge = graph[i][j];
				edge_node_1= i;
				edge_node_2= j;
			}
		}
	}
	// node which is nearest to the tree
	// if it is already in the tree, distance is 0 

}


int main()
{
	float graph[4][4]=
		{
			{I,  2, 1,1.5},
			{2,  I, I,  7},
			{1,  I, I,  8},
			{1.5,7, 8,  I}
		};
	
	std::vector<int> tree = minimum_cost_spanning_tree(graph,4);
	for(int i=0;i<tree.size();i++)
	{
		std::cout<<tree[i];
	}

}

#include <boost/locale.hpp>
#include <boost/algorithm/string/case_conv.hpp>
#include <iostream>
#include <ctime>



int main()
{
    using namespace boost::locale;
    // Create system default locale
    generator gen;
	std::locale loc=gen(""); 
	std::locale::global(loc); 
	std::cout.imbue(loc);

    
	std::cout<<"Correct case conversion can't be done by simple, character by character conversion"<<std::endl;
	std::cout<<"because case conversion is context sensitive and not 1-to-1 conversion"<<std::endl;
	std::cout<<"For example:"<<std::endl;
	std::cout<<"   German grüßen correctly converted to "<<to_upper("grüßen")<<", instead of incorrect "
                    <<boost::to_upper_copy(std::string("grüßen"))<<std::endl;
	std::cout<<"     where ß is replaced with SS"<<std::endl;
	std::cout<<"   Greek ὈΔΥΣΣΕΎΣ is correctly converted to "<<to_lower("ὈΔΥΣΣΕΎΣ")<<", instead of incorrect "
                    <<boost::to_lower_copy(std::string("ὈΔΥΣΣΕΎΣ"))<<std::endl;
	std::cout<<"     where Σ is converted to σ or to ς, according to position in the word"<<std::endl;
	std::cout<<"Such type of conversion just can be done using std::toupper that work on character base, also std::toupper is "<<std::endl;
	std::cout<<"not even applicable when working with variable character length like in UTF-8 or UTF-16 limiting the correct "<<std::endl;
	std::cout<<"behavior to unicode subset BMP or ASCII only"<<std::endl;
   
}
*/






/*
struct node 
{
	int key1=-1;
	int key2=-1;
	struct node* lchild;
	struct node* mchild;
	struct node* rchild;
};

struct node* root;

bool is_full(struct node* ptr_node);
struct node* insert(struct node* ptr_node, int key);
struct node* insert(struct node* ptr_node, int key)
{
	if(ptr_node ==nullptr)
	{
		struct node* temp = new node();
		temp->key1 = key;
		return temp;
	}

	if(!is_full(ptr_node))
	{
		if(key < ptr_node->key1)
		{
			ptr_node->key2=ptr_node->key1;
			ptr_node->key1=key;
		}
	}

	if(key < ptr_node->key1){ptr_node->lchild = insert(ptr_node->lchild,key);}
	if(key > ptr_node->key1 && key < ptr_node->key2)
	{
		ptr_node->mchild = insert(ptr_node->mchild,key);
	}
	if(key > ptr_node->key2){ptr_node->rchild = insert(ptr_node->rchild,key);}
	return ptr_node;
}


bool is_full(struct node* ptr_node)
{
	if(ptr_node->key1==-1){return false;}
	return true;

int main()
{
	std::cout<<"hello";

}


 *
#include <stdio.h>
    fork();
    fork();
    printf("Hello Liam!\n PID= %d\n",getpid());
 * */



