import shapely
from shapely.geometry import shape, Polygon,box, JOIN_STYLE
from shapely.ops import cascaded_union
import pdb
import math
from operator import itemgetter
# Calculation
def building(xmin,ymin,xmax,ymax,polys_design):
    
    gsize = 10 
    x_num = math.ceil((xmax-xmin) / gsize)
    y_num = math.ceil((ymax-ymin) / gsize)
    grids = []
    for i in range(x_num):
        for j in range(y_num):
            x0 = xmin + i * gsize
            x1 = xmin + (i+1)*gsize
            y0 = ymin + j * gsize
            y1 = ymin + (j+1)*gsize
            grids.append(box(x0, y0, x1, y1))


    s = [15,30,45] 
    volume = 0
    gfa = 0
    res_sqm = 0
    com_sqm = 0
    off_sqm = 0
    fs = {'commercial':0 ,'residential':0, 'office':0}

    volume3 = 0
    volume2com_res = 0
    volume2com_off = 0
    volume2res_off = 0
    volume1com = 0
    volume1res = 0
    volume1off = 0
    roof_surface = 0
    res_deck = 0


    for g_pos, grid in enumerate(grids):
        h_max=0.1
        i_area =[]
        functions = []
        f_height = []
        volume4all = {"com":[],"res":[],"off":[]}
        for p_pos, poly in enumerate(polys_design):
            polygon = poly['Polygon']
            # check if there are any polygons inside this grid
            i_id = 0
            h_id = 0
            if grid.intersects(polygon):
                i_area.append(grid.intersection(polygon).area)
                functions.append(poly["function"])
                f_height.append(poly["height"])

                # Find which kind of functional polygon it intersected with!
                if poly["function"] == "commercial":
                    volume4all["com"].append(poly["height"])
               
                elif poly["function"] == "residential":
                    volume4all["res"].append(poly["height"])
                elif poly["function"] == 'office':
                    volume4all["off"].append(poly["height"])

                for key, value in fs.items():
                    if key == poly["function"]:
                        fs[key] += gsize * gsize * poly["height"]/3

                h = poly["height"]
                if h > h_max:
                    h_max = h
                    h_id = i_id
                    i_id += 1


        if h_max != 0.1:
            h_grid = h_max
            area = i_area[h_id]
            gfa += area * h_grid/3
            volume += area * h_grid

        # 对此grid而言
        v_check = {k: v for k, v in volume4all.items() if v != []}

        if v_check != {}:
            garea = area
            for key, all_height in volume4all.items():
                segment =[]
                for val in all_height:
                    if val == 15:
                        segment.extend(["s1"])
                    elif val == 45:#135
                        segment.extend(["s1", "s2"])
                    elif val == 90:
                        segment.extend(["s1", "s2", "s3"])
                volume4all[key] = segment

            # 最底层
            s1_com = volume4all["com"].count("s1") # 2
            s1_res = volume4all["res"].count("s1") # 1
            s1_off = volume4all["off"].count("s1") # 1
            s1_count = s1_com+s1_res+s1_off
            # 中间层
            s2_com = volume4all["com"].count("s2")
            s2_res = volume4all["res"].count("s2")
            s2_off = volume4all["off"].count("s2")
            s2_count = s2_com+s2_res+s2_off
            # 最高层
            s3_com = volume4all["com"].count("s3")
            s3_res = volume4all["res"].count("s3")
            s3_off = volume4all["off"].count("s3")
            s3_count = s3_com+s3_res+s3_off

            #BOTOM LAYER
            # 一种相交
            # 第一层
            if (s1_com > 0) & (s1_res == 0) & (s1_off == 0):
                volume1com += (garea * s[0] / 3 * s1_com)/s1_count
                roof_surface += garea
            elif (s1_com == 0) & (s1_res > 0) & (s1_off == 0):
                volume1res += (garea * s[0] / 3 * s1_res)/s1_count
                roof_surface += garea
                res_deck += garea
            elif (s1_com == 0) & (s1_res == 0) & (s1_off > 0):
                volume1off += (garea * s[0] / 3 * s1_off)/s1_count
                roof_surface += garea
            # 两种相交
            # 第一层俩 com res off
            elif (s1_com > 0) & (s1_res > 0) & (s1_off == 0):
                volume2com_res += (garea * s[0] / 3 * (s1_com + s1_res))/s1_count
                res_sqm += volume2com_res * (s1_res/s1_count)
                com_sqm += volume2com_res * (s1_com/s1_count)
                roof_surface += garea
            elif (s1_com > 0) & (s1_res == 0) & (s1_off > 0):
                volume2com_off += (area * s[0] / 3 * (s1_com + s1_off))/s1_count
                com_sqm += volume2com_off * (s1_com / s1_count)
                off_sqm += volume2com_off * (s1_off / s1_count)
                roof_surface += garea
            elif (s1_com == 0) & (s1_res > 0) & (s1_off > 0):
                volume2res_off += (garea * s[0] / 3 * (s1_off + s1_res))/s1_count
                res_sqm += volume2res_off * (s1_res / s1_count)
                com_sqm += volume2res_off * (s1_com / s1_count)
                roof_surface += garea
            # 三种相交
            elif (s1_com > 0) & (s1_res > 0) & (s1_off > 0):
                volume3 += garea * s[0] / 3
                res_sqm += volume3 * s1_res/s1_count
                com_sqm += volume3 * s1_com / s1_count
                off_sqm += volume3 * s1_off / s1_count
                roof_surface += garea

            ## MIDDLE LAYER
            # 一种相交
            if (s2_com > 0) & (s2_res == 0) & (s2_off == 0):
                volume1com += (garea * s[1] / 3 * s2_com)/s2_count
            elif (s2_com == 0) & (s2_res > 0) & (s2_off == 0):
                volume1res += (garea * s[1] / 3 * s2_res)/s2_count
            elif (s2_com == 0) & (s2_res == 0) & (s2_off > 0):
                volume1off += (garea * s[1] / 3 * s2_off)/s2_count
            # 两种相交
            elif (s2_com > 0) & (s2_res > 0) & (s2_off == 0):
                volume2com_res += garea * s[1] / 3
                res_sqm += volume2com_res * (s2_res / s2_count)
                com_sqm += volume2com_res * (s2_com / s2_count)
            elif (s2_com > 0) & (s2_res == 0) & (s2_off > 0):
                volume2com_off += garea * s[1] / 3
                com_sqm += volume2com_off * (s2_com / s2_count)
                off_sqm += volume2com_off * (s2_off / s2_count)
            elif (s2_com == 0) & (s2_res > 0) & (s2_off > 0):
                volume2res_off += (garea * s[1] / 3 * (s2_off + s2_res))/s2_count
                res_sqm += volume2res_off * (s2_res / s2_count)
                com_sqm += volume2res_off * (s2_com / s2_count)
            # 三种相交
            elif (s2_com > 0) & (s2_res > 0) & (s2_off > 0):
                volume3 += garea * s[1] / 3
                res_sqm += volume3 * s2_res / s2_count
                com_sqm += volume3 * s2_com / s2_count
                off_sqm += volume3 * s2_off / s2_count

            ## TOPLAYER
            #一种相交
            if (s3_com > 0) & (s3_res == 0) & (s3_off == 0):
                volume1com += garea * s[2] / 3
            elif (s3_com == 0) & (s3_res > 0) & (s3_off == 0):
                volume1res += garea * s[2] / 3
            elif (s3_com == 0) & (s3_res == 0) & (s3_off > 0):
                volume1off += (garea * s[2] / 3 * s3_off)/s3_count
            # 两种相交
            elif (s3_com > 0) & (s3_res > 0) & (s3_off == 0):
                volume2com_res += garea * s[2] / 3
                res_sqm += volume2com_res * (s3_res / s3_count)
                com_sqm += volume2com_res * (s3_com / s3_count)
            elif (s3_com > 0) & (s3_res == 0) & (s3_off > 0):
                volume2com_off += garea * s[2] / 3
                com_sqm += volume2com_off * (s3_com / s3_count)
                off_sqm += volume2com_off * (s3_off / s3_count)
            elif (s3_com == 0) & (s3_res > 0) & (s3_off > 0):
                volume2res_off += garea * s[2] / 3
                res_sqm += volume2res_off * (s3_res / s3_count)
                com_sqm += volume2res_off * (s3_com / s3_count)
            # 三种相交
            elif (s3_com > 0) & (s3_res > 0) & (s3_off > 0):
                volume3 += garea * s[2] / 3
                res_sqm += volume3 * s3_res / s3_count
                com_sqm += volume3 * s3_com / s3_count
                off_sqm += volume3 * s3_off / s3_count



    print("volume3",volume3)
    print("mixed used,(comres,comoff,resoff)",volume2com_res,volume2com_off,volume2res_off)
    print("single used:(com, off, res)",volume1com,volume1off,volume1res)

    return volume3,volume2com_res,volume2com_off,volume2res_off,volume1com,volume1off,volume1res,roof_surface,res_deck