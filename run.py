"""一键运行脚本"""
import subprocess
import sys
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent
REPORT_DIR = PROJ_ROOT / "reports"


def run_tests(env: str = "test", markers: str = "", extra_args: str = ""):
    """运行测试并生成 Allure 报告"""
    cmd = [
        sys.executable, "-m", "pytest",
        f"--env={env}",
    ]

    if markers:
        cmd.extend(["-m", markers])

    if extra_args:
        cmd.extend(extra_args.split())

    print(f"{'='*60}")
    print(f"  环境: {env}")
    print(f"  标记: {markers or '全部'}")
    print(f"  命令: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, cwd=PROJ_ROOT)
    return result.returncode


def serve_allure():
    """启动 Allure 报告服务器"""
    result_dir = REPORT_DIR / "allure-results"
    if not result_dir.exists():
        print("❌ 未找到 Allure 结果目录，请先运行测试")
        return 1

    print("🌐 正在启动 Allure 报告服务...")
    subprocess.run(["allure", "serve", str(result_dir)], cwd=PROJ_ROOT)
    return 0


def generate_report():
    """生成静态 Allure 报告"""
    result_dir = REPORT_DIR / "allure-results"
    report_dir = REPORT_DIR / "allure-report"
    subprocess.run([
        "allure", "generate", str(result_dir),
        "-o", str(report_dir),
        "--clean",
    ], cwd=PROJ_ROOT)
    print(f"✅ 报告已生成: {report_dir / 'index.html'}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="API 测试框架运行器")
    parser.add_argument("--env", default="test", help="环境: dev/test/staging/prod")
    parser.add_argument("-m", "--markers", default="", help="pytest 标记过滤")
    parser.add_argument("--serve", action="store_true", help="运行后启动 Allure 报告")
    parser.add_argument("--generate", action="store_true", help="生成静态 Allure 报告")
    parser.add_argument("args", nargs="*", help="额外 pytest 参数")

    args = parser.parse_args()

    code = run_tests(env=args.env, markers=args.markers, extra_args=" ".join(args.args))

    if code == 0 and args.serve:
        serve_allure()
    elif code == 0 and args.generate:
        generate_report()

    sys.exit(code)
