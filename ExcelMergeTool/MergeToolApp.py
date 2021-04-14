import sys
import os
from scr.Helper.CopyHelper import FileCopyHelper
from scr.Reader.ExcelMergeMain import ExcelMergeMain
import scr.Helper.DebugHelper as DebugHelper
import scr.Helper.LogFileHelper as LogFileHelper
import traceback

#python mergetoolapp.py G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Base.xlsm G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Mine.xlsm G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Their.xlsm

print("*****************************************************************************")
print("*                           Excel合并工具                                   *")
print("*****************************************************************************")
def pause():
    DebugHelper.Log("输入任意键继续")
    message = input()

# path_modify = dict(
#     base = sys.argv[-1],
#     mine = sys.argv[-2],
#     their = sys.argv[-3],
#     merge = sys.argv[-4],)

path_modify = dict(
    merge = "G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Merge.xlsm",
    their = "G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Their.xlsm",
    mine = "G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Mine.xlsm",
    base = "G:\ACGScript\github\ExcelMergeTool-master\ExcelMergeTool\DebugCacheFile\Base.xlsm",
)

def main(path_modify):
    mine_copy_helper = FileCopyHelper(path_modify["base"])
    print("pre: " + path_modify["their"])
    their_copy_helper = FileCopyHelper(path_modify["their"])
    print("after: " + their_copy_helper.copypath)

    path_modify["base"] = mine_copy_helper.copypath
    path_modify["their"] = their_copy_helper.copypath

    # 提问，为哈base 与 their 被复制了，但是my却没有
    # 回答，印象是 base 与 their 会被svn命名为 sth.xlsx.r[number], 所以额外处理一蛤

    merger = ExcelMergeMain(path_modify["merge"],path_modify["their"],path_modify["mine"],path_modify["base"])
    result = merger.StartWork()
    merger.OnRelease()
    if result:
        #如果检查通过 并合并 那就把base和their删除掉
        DebugHelper.Log("【合并成功】")
        mine_copy_helper.DelSourceFile()
        their_copy_helper.DelSourceFile()
    mine_copy_helper.OnRelease()
    their_copy_helper.OnRelease()

def CheckPath():
    global path_modify
    for path in path_modify.values():
        if not os.path.exists(path):
            DebugHelper.LogColor(DebugHelper.FontColor.red,"对象文件不存在，请检查是否已经处理完毕 ",path)
            return False
    return True

#只允许存在一个窗口
if LogFileHelper.IsExist(path_modify["mine"]):
    DebugHelper.LogColor(DebugHelper.FontColor.red,"已经有一个程序窗口在运行！！！")
    pause()
    sys.exit()

LogFileHelper.InitLogFile(path_modify["mine"])
if __name__ == '__main__':
    try:
        if CheckPath():
            main(path_modify)
    except Exception as e:
        print(e.args)
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
LogFileHelper.ReleaseLogFile()
pause()
LogFileHelper.DelLogFile()