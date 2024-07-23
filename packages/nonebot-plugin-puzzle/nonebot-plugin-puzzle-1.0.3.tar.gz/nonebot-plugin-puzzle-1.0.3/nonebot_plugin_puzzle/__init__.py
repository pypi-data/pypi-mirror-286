from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from puzzle_rs import PuzzleCore as Puzzle
from .render import Render
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .rank import add_point, get_rank, get_point

group_id_list_cache, obj_cache, group_id_list, obj_dist = [], {}, [], {}
direction_list, mode_list, mode_dist = ['U', 'D', 'L', 'R'], ['8', '15', '24'], {'8': 3, '15': 4, '24': 5}
render_list = [Render(3), Render(4), Render(5)]

hrd = on_command('puzzle', aliases={'华容道', 'pz'}, priority=32)  # 新游戏


@hrd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    group_id = event.group_id
    uid = event.user_id
    if group_id not in group_id_list:
        if args.extract_plain_text() not in mode_list:
            await hrd.finish('请在命令后面加上模式，可选模式8 15 24')
        group_id_list.append(group_id)
        puzzle = Puzzle(mode_dist[args.extract_plain_text()])

        exec(f"obj_dist[{group_id}] = puzzle")

        buf = render_list[puzzle.get_mode() - 3].get_buf(puzzle.get_puzzle())
        img = MessageSegment.image(buf.getvalue())
        await hrd.finish(img)
        buf.close()
    if args.extract_plain_text() in mode_list:
        await hrd.finish(f"已存在游戏,请发送pz结束,结束当前游戏～")
    if args.extract_plain_text() == '结束':
        group_id_list.remove(group_id)
        await hrd.finish("游戏结束")
    puzzle = obj_dist[group_id]
    mode = puzzle.get_mode()
    plain_texts = args.extract_plain_text()  # 命令匹配

    done = puzzle.move_sequence(plain_texts)
    if done:
        add_point(group_id=group_id, uid=uid, name=event.sender.nickname, mode=mode)
        buf = render_list[mode - 3].get_buf(puzzle.get_puzzle())
        points = get_point(uid=uid, group=group_id, mode=mode)
        await hrd.finish(f"执行操作{puzzle.get_cmds_str()}\n已还原,用时：{puzzle.duration()}\n获得积分1,当前积分{points}\n" +
                         MessageSegment.image(buf.getvalue()))
        group_id_list.remove(group_id)
        buf.close()
    else:
        buf = render_list[mode - 3].get_buf(puzzle.get_puzzle())
        await hrd.finish(f"执行操作{puzzle.get_cmds_str()}\n用时：{puzzle.duration()}\n" +
                         MessageSegment.image(buf.getvalue()))
        buf.close()


rank_puzzle = on_command("rankpuzzle", aliases={'华容排名', 'rankpz'}, priority=20)


@rank_puzzle.handle()
async def send_rank(event: GroupMessageEvent, args: Message = CommandArg()):  # 发送群排名
    if args.extract_plain_text() not in mode_list:
        await rank_puzzle.finish('请在命令后面加上模式，可选模式8 15 24')
    rank_text = get_rank(event.group_id, mode=mode_dist[args.extract_plain_text()])
    await rank_puzzle.finish(rank_text)
