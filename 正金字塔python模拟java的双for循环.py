def print_pyramid(n):
    for i in range(1, n + 1):
        # 打印前导空格不去換行
        print(' ' * (n - i), end=' ')
        # 打印星号
        print('*' * (2 * i - 1))

# 调用函数，打印高度为5的金字塔
print_pyramid(5)
#javapackage com.southwind.util;
'''
public class ArrestCrimer{
    public static void printPyramid(int n) {
        for (int i = 1; i <= n; i++) {
            // 打印前导空格
            for (int j = 1; j <= n - i; j++) {
                System.out.print(" ");
            }
            // 打印星号
            for (int j = 1; j <= 2 * i - 1; j++) {
                System.out.print("*");
            }
            // 换行
            System.out.println();
        }
    }

    public static void main(String[] args) {
        // 调用函数，打印高度为5的金字塔
        printPyramid(5);
    }
}
'''
