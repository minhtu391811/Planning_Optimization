#include<bits/stdc++.h>
using namespace std;

int n;
int visited[10001] = {0};
int pos[10001] = {0};

void Try(int k){
	if(k == n+1){
		cout << n << '\n';
		for(int i = 1; i <= n; i++){
			cout << pos[i] << ' ';
		}
		exit(0);
	}
	for(int i = 1; i <= n; i++){
		if(visited[i]) continue;
		int flag = 0;
		for(int j = 1; j < k; j++){
			if (i - pos[j] == k - j || i - pos[j] == j - k){
				flag = 1;
				break;
			}
		}
		
		if (flag) continue; 
		else{
			pos[k] = i;
			visited[i] = 1;
			Try(k+1);
			visited[i] = 0;
		}
	}
}


int main(){
	ios_base::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
	cin >> n;
	if (n <= 20){
//		cout << "djm";
		Try(1);
	}
	else{
		cout << n << '\n';
		for(int i = 1; i <= n; i++){
			cout << i << ' ';
		}
	}
}