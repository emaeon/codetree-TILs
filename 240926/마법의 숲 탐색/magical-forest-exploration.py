import sys

input = sys.stdin.readline

r, c, k = map(int, input().split())
unit = [list(map(int, input().split())) for _ in range(k)]  # 골렘
arr = [[1] + [0] * c + [1] for _ in range(r + 3)] + [[1] * (c + 2)]
exit_set = set()

# 상 우 하 좌 (동쪽 : 시계 방향)
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


def bfs(si,sj):
    q = []
    v = [[0] + [0] * c + [0] for _ in range(r + 3)] + [[0] * (c + 2)]
    mx_i = 0 #-2해서 리턴!

    q.append((si,sj))
    v[si][sj] = 1

    while q :
        ci,cj = q.pop(0)
        #정답처리
        mx_i = max(mx_i, ci)


        # 네방향, 미방문, 조건 : 같은 값 또는 내가 출구 - 상대방이 골렘
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)) :
            ni,nj = ci+di, cj+dj
            if not v[ni][nj] and ((arr[ci][cj] == arr[ni][nj]) or ((ci,cj) in exit_set and arr[ni][nj] > 1)):
                q.append((ni,nj))
                v[ni][nj] = 1
    return mx_i -2



ans = 0
num = 2  # 골렘번호
# unit(골렘) 개수 만큼 입력 좌표, 방향에 따라서 남쪽 이동 및 정령 최대좌표 계산
for cj, dr in unit:
    ci = 1  # 맨 처음 시작 중심좌표
    # 남쪽으로 최대한 이동 (남 - 서 - 동)
    while True:
        # 남쪽
        if (arr[ci + 1][cj - 1] + arr[ci + 2][cj] + arr[ci + 1][cj + 1]) == 0:  # 비어있음
            ci += 1
            # 서족으로 회전하면서 아래로 한칸
        elif (arr[ci - 1][cj - 1] + arr[ci][cj - 2] + arr[ci + 1][cj - 1] + arr[ci + 1][cj - 2] + arr[ci + 2][
            cj - 1]) == 0:  # 비어있음
            ci += 1
            cj -= 1
            dr = (dr - 1) % 4
        # 동쪽으로 회전하면서 아래로 한칸
        elif (arr[ci - 1][cj + 1] + arr[ci][cj + 2] + arr[ci + 1][cj + 1] + arr[ci + 1][cj + 2] + arr[ci + 2][
            cj + 1]) == 0:  # 비어있음
            ci += 1
            cj += 1
            dr = (dr + 1) % 4
        else:
            break

    # 2 골렘 표시
    if ci < 4:  # 몸이 범위 밖
        arr = [[1] + [0] * c + [1] for _ in range(r + 3)] + [[1] * (c + 2)]
        exit_set = set()
        num = 2 #안그러면 번호가 너무 올라감~

    else:
        #골렘을 표시 + 비상구 위치 추가
        arr[ci + 1][cj] = arr[ci - 1][cj] = num
        arr[ci][cj - 1:cj + 2] = [num] * 3
        num += 1

        exit_set.add((ci+di[dr], cj+dj[dr]))
        #남쪽으로 가기
        ans += bfs(ci,cj)


print(ans)