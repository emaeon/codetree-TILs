import sys

input = sys.stdin.readline

n,m,k = map(int,input().split()) #미로크기, 참가자 수, 게임 시간
arr = []
for _ in range(n) :
    arr.append(list(map(int, input().split())))
for _ in range(m):
    ti,tj = map(lambda x : int(x)-1, input().split())
    arr[ti][tj] -= 1

ei,ej = map(lambda x : int(x)-1,input().split())
arr[ei][ej] = -11

def find_sqr(arr) :
    #[1] 비상구와 모든 사람간 가장 짧은 가로 혹은 세로 거리 구하기 -> L
    mn = n
    for i in range(n) :
        for j in range(n) :
            if -11<arr[i][j]<0:
                mn = min(mn, max(abs(ei-i), abs(ej-j)))

    #[2] (0,0) 부터 순회하면서 길이 L인 정사각형에 비상구와 사람있는지 체크 -> 리턴 L +1
    for si in range(n-mn):
        for sj in range(n-mn) :
            if si <= ei <= si+mn and sj <= ej <= sj+mn :
                for i in range(si, si+mn+1):
                    for j in range(sj, sj+mn+1) :
                        if -11 < arr[i][j] < 0 :
                            return si,sj, mn+1


def find_exit(arr) :
    for i in range(n) :
        for j in range(n) :
            if arr[i][j] == -11 :
                return i,j


# k 턴 또는 모두 탈출까지 모든 사람의 이동거리 누적
ans = 0
cnt = m

for _ in range(k):
    #[1] 모든 참가자가 동시에 한 칸 이동 (출구 최단거리 방향 상/하 우선)
    # 출구 도착하면 즉시 탈출
    narr= [x[:] for x in arr]
    for i in range(n) :
        for j in range(n) :
            if -11<arr[i][j]<0 :#사람인 경우
                dist = abs(ei-i)+abs(ej-j)
                # 네방향(상하우선), 범위 내, 벽 아니고 <=0, 거리가 dist보다 작으면
                for di, dj in ((-1,0),(1,0),(0,-1),(0,1)) :
                    ni, nj = i+di, j+dj
                    if 0<=ni<n and 0<=nj<n and arr[ni][nj]<=0 and dist>(abs(ei-ni)+abs(ej-nj)):
                        ans += arr[i][j] #현재  인원수가 이동하는 것이니 이동거리에 누적
                        narr[i][j] -= arr[i][j] #더하면 안됨, 이동처리
                        if arr[ni][nj] == -11 : #비상구라면
                            cnt += arr[i][j] # 탈출!
                        else : #일반 빈칸이거나 사람이면
                            narr[ni][nj] += arr[i][j] #들어온 인원 추가
                        break
    arr = narr
    if cnt == 0 :
        break


    #[2] 미로회전
    si,sj,L = find_sqr(arr)

    narr = [x[:] for x in arr]
    for i in range(L):
        for j in range(L) :
            narr[si+i][sj+j] = arr[si+L-1-j][sj+i]
            if narr[si+i][sj+j] > 0 : #벽이면 회전하면서 -1
                narr[si+i][sj+j] -= 1
    arr = narr
    #회전으로 달라져서 비상구 위치 저장
    ei,ej = find_exit(arr)

print(-ans)
print(ei+1,ej+1)