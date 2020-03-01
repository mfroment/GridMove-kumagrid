import os
from vrectangle import Vrectangle
from fractions import Fraction as _F
from itertools import accumulate


def __main__():
    # see doc folder for layout

    # (hard-coded) inputs:
    outfile = os.path.join("_out_", "kumagrid.grid")
    n_monitors = 2
    # the target sequences of grid widths/heigths, and their top/left anchor (wrt to monitor 'canvas')
    intervals = [_F(1, 3), _F(1, 2), _F(2, 3), _F(1, 3), _F(2, 3), _F(1, 2), _F(1, 3)]
    grid_starts = [0, 0, 0, _F(1, 3), _F(1, 3), _F(1, 2), _F(2, 3)]

    # ------------
    # sequence of bottom/right anchors (wrt to monitor 'canvas'
    grid_ends = [x + y for x, y in zip(intervals, grid_starts)]
    # normalized intervals, used for trigger sizing ; and trigger anchors (wrt to trigger canvas)
    ratios = [x / sum(intervals) for x in intervals]
    trigger_ends = list(accumulate(ratios))
    trigger_starts = [0]+trigger_ends[:-1]

    # get trigger canvases for the respective 4 grid sections (fullscreen, columns, rows, cells)
    trigger_canvases = get_trigger_canvases(_F(1, 50), intervals)

    # get grid trigger definitions as Vrectangles
    grid_trigger_defs = get_grid_trigger_defs(grid_starts, grid_ends, trigger_starts, trigger_ends, trigger_canvases)

    # build the grid file contents
    grid_rules = get_grid_rules(grid_trigger_defs, n_monitors)

    # write to file
    f = open(outfile, "w")
    [ f.write(line + "\n") for line in grid_rules ]
    f.close()



def get_trigger_canvases(margin, intervals):
    base_canvas = Vrectangle(margin, margin, 1-margin, 1-margin)

    spans = { 'vector': max(intervals), 'cells': sum(intervals), 'inner_margin': min(intervals)*_F(2,3) }
    # area is split in vector/inner_margin/cells/(ghost)inner_margin/(ghost)vector
    # (ghost spans serve to center the cells)
    area_span = spans['vector']*2 + spans['cells'] + spans['inner_margin']*2
    spans = { k: v / area_span for k, v in spans.items() } # normalize
    # anchors for sections:
    anchors = [
        0,
        spans['vector'],
        spans['vector'] + spans['inner_margin'],
        spans['vector'] + spans['inner_margin'] + spans['cells']
    ]
    return {
        'fullscreen': Vrectangle(anchors[0], anchors[0], anchors[1], anchors[1], base_canvas),
        'columns': Vrectangle(anchors[0], anchors[2], anchors[1], anchors[3], base_canvas),
        'rows': Vrectangle(anchors[2], anchors[0], anchors[3], anchors[1], base_canvas),
        'cells': Vrectangle(anchors[2], anchors[2], anchors[3], anchors[3], base_canvas)
    }


def get_grid_trigger_defs(grid_starts, grid_ends, trigger_starts, trigger_ends, trigger_canvases):
    res = []
    # fullscreen
    res += get_grid_trigger_def_section([0], [0], [1], [1],
                                        [0], [0], [1], [1],
                                        trigger_canvases['fullscreen'])
    # columns
    res += get_grid_trigger_def_section([0], grid_starts, [1], grid_ends,
                                        [0], trigger_starts, [1], trigger_ends,
                                        trigger_canvases['columns'])
    # rows
    res += get_grid_trigger_def_section(grid_starts, [0], grid_ends, [1],
                                        trigger_starts, [0], trigger_ends, [1],
                                        trigger_canvases['rows'])
    # cells
    res += get_grid_trigger_def_section(grid_starts, grid_starts, grid_ends, grid_ends,
                                        trigger_starts, trigger_starts, trigger_ends, trigger_ends,
                                        trigger_canvases['cells'])
    return res


def get_grid_trigger_def_section(grid_tops, grid_lefts, grid_bottoms, grid_rights,
                                 trigger_tops, trigger_lefts, trigger_bottoms, trigger_rights,
                                 trigger_canvas):
    assert(len(grid_tops) == len(grid_bottoms) == len(trigger_tops) == len(trigger_bottoms))
    assert(len(grid_lefts) == len(grid_rights) == len(trigger_lefts) == len(trigger_rights))
    res = []
    for grid_top, grid_bottom, trigger_top, trigger_bottom \
            in zip(grid_tops, grid_bottoms, trigger_tops, trigger_bottoms):
        for grid_left, grid_right, trigger_left, trigger_right \
                in zip(grid_lefts, grid_rights, trigger_lefts, trigger_rights):
            res.append({
                'grid': Vrectangle(grid_top, grid_left, grid_bottom, grid_right),
                'trigger': Vrectangle(trigger_top, trigger_left, trigger_bottom, trigger_right, trigger_canvas)
            })
    return res


def get_grid_trigger_rule(index, grid_trigger_def, monitor = 1):
    reframed_grid = grid_trigger_def['grid'].reframe()
    reframed_trigger = grid_trigger_def['trigger'].reframe()
    res = [
        f"[{index}]",
        "",
        f"  TriggerTop    = [MonitorReal{monitor}Top]" +
            ("" if reframed_trigger.top == 0 else f"    + [MonitorReal{monitor}Height] * {reframed_trigger.top}"),
        f"  TriggerLeft   = [MonitorReal{monitor}Left]" +
            ("" if reframed_trigger.left == 0 else f"   + [MonitorReal{monitor}Width] * {reframed_trigger.left}"),
        f"  TriggerBottom = [MonitorReal{monitor}Bottom]" +
            ("" if reframed_trigger.bottom == 1 else f" - [MonitorReal{monitor}Height] * {1-reframed_trigger.bottom}"),
        f"  TriggerRight  = [MonitorReal{monitor}Right]" +
            ("" if reframed_trigger.right == 1 else f"  - [MonitorReal{monitor}Width] * {1 - reframed_trigger.right}"),
        "",
        f"  GridTop       = [Monitor{monitor}Top]" +
            ("" if reframed_grid.top == 0 else f"        + [Monitor{monitor}Height] * {reframed_grid.top}"),
        f"  GridLeft      = [Monitor{monitor}Left]" +
            ("" if reframed_grid.left == 0 else f"       + [Monitor{monitor}Width] * {reframed_grid.left}"),
        f"  GridBottom    = [Monitor{monitor}Bottom]" +
            ("" if reframed_grid.bottom == 1 else f"     - [Monitor{monitor}Height] * {1-reframed_grid.bottom}"),
        f"  GridRight     = [Monitor{monitor}Right]" +
            ("" if reframed_grid.right == 1 else f"      - [Monitor{monitor}Width] * {1 - reframed_grid.right}"),
        ""
    ]
    return res


def get_grid_rules(grid_trigger_defs, n_monitors):
    res = [
        "[Groups]",
        "",
        f"  NumberOfGroups = {n_monitors*len(grid_trigger_defs)}",
        "",
    ]
    rule_index = 1
    for monitor in list(range(1, n_monitors+1)):
        for grid_trigger_def in grid_trigger_defs:
            res += get_grid_trigger_rule(rule_index, grid_trigger_def, monitor)
            rule_index += 1
    # res += [
    #     f"[{rule_index}]",
    #     "",
    #     f"  TriggerTop    = [MonitorReal{monitor}Top]",
    #     f"  TriggerLeft   = [MonitorReal{monitor}Left]",
    #     f"  TriggerBottom = [MonitorReal{monitor}Bottom]",
    #     f"  TriggerRight  = [MonitorReal{monitor}Right]",
    #     "",
    #     f"  GridTop       = Restore",
    #     f"  GridLeft      = Restore",
    #     f"  GridBottom    = Restore",
    #     f"  GridRight     = Restore",
    #     ""
    # ]
    return res



if __name__ == "__main__":
    __main__()