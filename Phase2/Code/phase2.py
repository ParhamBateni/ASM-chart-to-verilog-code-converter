from tkinter import *
from tkinter import messagebox
import tkinter as tk

default_font='Helvetica 9 bold'
window_width=800
window_height=800

rectangle_width=120
rectangle_height=60

oval_r1=120
oval_r2=80

description_box_width=25
description_box_height=5

box_distance=25

button_height=1
button_width=5

global main_canvas,description_box

side_canvas_height=175
side_canvas_width=window_width-20

global run_button,delete_box_button,add_shape_button,add_right_button,add_left_button,add_mode_right,delete_route_button
global state_box_icon,condition_box_icon,decision_box_icon

global scale
scale=1

global graph
global all_blocks
all_blocks = dict()

class Block:
    def __init__(self):
        self.block_type = None
        self.all_lines = []
        self.next_block = None  # 1 True
        self.next_next_block = None  # 0 False
        self.empty = False

    def __str__(self):
        print("Block: ", self.block_type)
        print("lines = ")
        for line in self.all_lines:
            print("line = ", line)
        if self.next_block:
            print("self.next_block = ", self.next_block)
        if self.next_next_block:
            print("self.next_next_block = ", self.next_next_block)
        return ""

class ASMGraph:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.box_connections = dict()

    def add_box(self, _type):
        global add_mode_right,route_mode,add_mode
        #check to if the box is decision and the selected box has child don't add the box
        if route_mode.get() or not add_mode.get():
            messagebox.showinfo("Addition error", "You can't add a box in routing mode(change the mode)")
            return
        elif _type=="decision" and ASMBox.selected_box is not None:
            if ASMBox.selected_box.type=="decision":
                if add_mode_right.get() and ASMBox.selected_box.child_boxes[1]!=None:
                    messagebox.showinfo("Addition error",
                                        "You can't add a decision box in this position(delete the connected boxes)")
                    return
                elif not add_mode_right.get() and ASMBox.selected_box.child_boxes[0]!= None:
                    messagebox.showinfo("Addition error",
                                        "You can't add a decision box in this position(delete the connected boxes)")
                    return
            else:
                if ASMBox.selected_box.child_boxes!=[None ,None]:
                    messagebox.showinfo("Addition error",
                                        "You can't add a decision box in this position(delete the connected boxes)")
                    return
        elif ASMBox.selected_box is not None and (ASMBox.selected_box.route_arrows[1]!= None and add_mode_right.get() \
            or ASMBox.selected_box.route_arrows[0]!=None and not add_mode_right.get()):
            messagebox.showinfo("Addition error",
                                "You can't add a box in this position(delete the connected boxes)")
            return
        box = ASMBox(self, _type)
        moved = False
        if ASMBox.selected_box is not None:
            # print(f"dfs result on {ASMBox.selected_box}:")
            # print(self.dfs_search(ASMBox.selected_box,{}))
            if ASMBox.selected_box.type=="decision":
                if add_mode_right.get():
                    children=self.dfs_search(ASMBox.selected_box.child_boxes[1],{})
                    if ASMBox.selected_box.child_boxes[1] is not None:
                        children.append(ASMBox.selected_box.child_boxes[1])
                else:
                    children=self.dfs_search(ASMBox.selected_box.child_boxes[0],{})
                    if ASMBox.selected_box.child_boxes[0] is not None:
                        children.append(ASMBox.selected_box.child_boxes[0])

            else:
                children=self.dfs_search(ASMBox.selected_box,{})
            # print(f"dfs result on {ASMBox.selected_box} is {children}")
            # print(f"box connections are {self.box_connections}")
            for child_box in children:
                # print(f"box is {child_box} and parent arrow is {child_box.parent_arrow}")
                moved = True
                self.canvas.move(child_box.id, 0, box.height + box_distance )
                self.canvas.move(child_box.number_text_id,0,box.height+box_distance)
                for route in child_box.route_arrows:
                    if route==None:continue
                    self.canvas.move(route,0,box.height+box_distance)
                for route_text in child_box.route_arrows_text_ids:
                    if route_text==None:continue
                    self.canvas.move(route_text,0,box.height+box_distance)
                if child_box.text_id is not None:
                    self.canvas.move(child_box.text_id,0,box.height+box_distance)
                child_box.y+=box.height+box_distance
                try:
                    self.canvas.move(child_box.parent_arrow,0,box.height+box_distance)
                except:
                    continue
        if ASMBox.selected_box is not None:
            direction = "right" if add_mode_right.get() and ASMBox.selected_box.type == "decision" else "left"
            direction_index=0 if direction=="left" else 1
        else:
            direction="left"
            direction_index=0
        # print(f"direction in {direction} mode is {add_mode_right.get()}")

        if ASMBox.selected_box is not None and ASMBox.selected_box.route_arrows[direction_index]!=None:
            route_arrow=ASMBox.selected_box.route_arrows[direction_index]
            self.canvas.move(route_arrow,0,box.height+box_distance)
            ASMBox.selected_box.route_arrows[direction_index]=None
            box.route_arrows[direction_index]=route_arrow
            route_arrow_text=ASMBox.selected_box.route_arrows_text_ids[direction_index]
            self.canvas.move(route_arrow_text,0,box.height+box_distance)
            ASMBox.selected_box.route_arrows_text_ids[direction_index]=None
            box.route_arrows_text_ids[direction_index] = route_arrow_text
        arrow = self.canvas.create_line(box.x + box.width / 2, box.y-box.height-box_distance, box.x + box.width / 2,
                                        box.y-box.height, arrow=tk.LAST)

        if ASMBox.selected_box is not None:
            # print(f"box is {box}")
            selected_child_box=self.box_connections[ASMBox.selected_box][direction_index]
            self.add_box_connection(box, self.box_connections[ASMBox.selected_box][direction_index])
            self.add_box_connection(ASMBox.selected_box, box,direction)
            if selected_child_box is not None:
                selected_child_box.parent_boxes.remove(ASMBox.selected_box)

        if moved:
            out_arrow=ASMBox.selected_box.child_arrows[direction_index]
            ASMBox.selected_box.set_child_arrow(arrow,direction)
            box.set_parent_arrow(arrow)
            box.set_child_arrow(out_arrow,direction)
        else:
            if ASMBox.selected_box is not None:
                ASMBox.selected_box.set_child_arrow(arrow,direction)
                # print(f"selected box child arrows are {ASMBox.selected_box.child_arrows}")
            box.set_parent_arrow(arrow)
            # print(f"box parent arrow is {box.parent_arrow}")
            # print(f"box child arrows are {box.child_arrows}\n")
        box.select_box()

        scroll_region = float(self.canvas['scrollregion'].split(" ")[3])
        x_right_scroll_region = max(float(self.canvas['scrollregion'].split(" ")[2]),self.get_the_most_right_box_x())+box_distance
        x_left_scroll_region = min(float(self.canvas['scrollregion'].split(" ")[0]),self.get_the_most_left_box_x())-box_distance
        lowest_box_y=self.get_lowest_box_y()
        self.canvas['scrollregion'] = (
        x_left_scroll_region, 0, x_right_scroll_region, max(scroll_region,lowest_box_y+box_distance))
        if ASMBox.selected_box.y > max(scroll_region,lowest_box_y+box_distance) * self.canvas.yview()[1]:
            self.canvas.yview_moveto(ASMBox.selected_box.y/ max(scroll_region,lowest_box_y+box_distance))

        # print(self.box_connections)

    def delete_box(self):
        global route_mode
        if route_mode.get():
            messagebox.showinfo("Deletion error","You can't delete a box in routing mode(change the mode)")
            return
        if self.self_loop_happens():
            messagebox.showinfo("Deletion error","You can't delete this box because this deletion leads to a self loop(delete the route)")
            return
        deleted_box_width=ASMBox.selected_box.width
        deleted_box_height=ASMBox.selected_box.height
        try:
            next_selected_box = ASMBox.selected_box.parent_boxes[0]
        except:
            try:
                next_selected_box = ASMBox.selected_box.child_boxes[0]
            except:
                next_selected_box = None
        input_arrow = ASMBox.selected_box.parent_arrow
        # print(f"input arrow is {input_arrow}")
        output_arrow =ASMBox.selected_box.child_arrows[0]
        # print(f"output arrows are {output_arrow}")
        # print(f"parent boxes {ASMBox.selected_box.parent_boxes}")
        # print(f"child boxes {ASMBox.selected_box.child_boxes}")
        for parent in ASMBox.selected_box.parent_boxes:
            if parent.route_arrows[0] != None:
                if parent.child_boxes[0] == ASMBox.selected_box:
                    # print("wow1")
                    self.canvas.itemconfig(parent.route_arrows_text_ids[0],
                                           text=str(ASMBox.selected_box.child_boxes[0].custom_id))
            if parent.route_arrows[1] != None:
                if parent.child_boxes[1] == ASMBox.selected_box:
                    # print("wow2")
                    self.canvas.itemconfig(parent.route_arrows_text_ids[1],
                                           text=str(ASMBox.selected_box.child_boxes[0].custom_id))
        for parent in ASMBox.selected_box.parent_boxes:
            try:
                parent.child_arrows[parent.child_arrows.index(input_arrow)]=None
                # print("did it change?")
                # print(parent.child_arrows,end="\n")
            except Exception as e:
                # print("here2")
                # print(e)
                pass
            parent.child_arrows[parent.child_boxes.index(ASMBox.selected_box)] = output_arrow
            try:
                parent.child_boxes[parent.child_boxes.index(ASMBox.selected_box)] = ASMBox.selected_box.child_boxes[0]
            except Exception as e:
                # print("here22")
                # print(e)
                pass


            # print(f"{parent} is a parent for {ASMBox.selected_box}")
            # print(f"parent child boxes are {parent.child_boxes}")

            # print(f"parent child arrows are {parent.child_arrows}")
        for child in ASMBox.selected_box.child_boxes:
            if child is None:continue
            # print(f"child is {child} and its parent boxes are {child.parent_boxes}")
            child.parent_boxes.remove(ASMBox.selected_box)
            child.parent_boxes.extend(ASMBox.selected_box.parent_boxes)

        for child_box in self.dfs_search(ASMBox.selected_box,{}):
            # print(f"child box {child_box} moved")
            self.canvas.move(child_box.id,  0, -(ASMBox.selected_box.height + box_distance))
            self.canvas.move(child_box.number_text_id,0,-(ASMBox.selected_box.height+box_distance))
            for route in child_box.route_arrows:
                if route == None: continue
                self.canvas.move(route, 0,-(ASMBox.selected_box.height + box_distance))
            for route_text in child_box.route_arrows_text_ids:
                if route_text == None: continue
                self.canvas.move(route_text, 0,-(ASMBox.selected_box.height + box_distance))
            if child_box.text_id is not None:
                self.canvas.move(child_box.text_id,0,-(ASMBox.selected_box.height+box_distance))
            child_box.y-=(ASMBox.selected_box.height+box_distance)
            try:
                self.canvas.move(child_box.parent_arrow, 0, -(ASMBox.selected_box.height + box_distance))
            except:
                continue
        if ASMBox.selected_box is not None and ASMBox.selected_box.route_arrows != [None, None]:
            for i,route_arrow in enumerate(ASMBox.selected_box.route_arrows):
                if route_arrow is None: continue
                self.canvas.move(route_arrow, 0, -(ASMBox.selected_box.height+box_distance))
            for i,route_arrow_text in enumerate(ASMBox.selected_box.route_arrows_text_ids):
                if route_arrow_text is None: continue
                self.canvas.move(route_arrow_text, 0, -(ASMBox.selected_box.height+box_distance))
        self.canvas.delete(ASMBox.selected_box.id)
        self.canvas.delete(input_arrow)
        self.canvas.delete(ASMBox.selected_box.number_text_id)


        for key in self.box_connections.copy():
            if self.box_connections[key].__contains__(ASMBox.selected_box):
                self.box_connections[key][self.box_connections[key].index(ASMBox.selected_box)]=self.box_connections[ASMBox.selected_box][0]
        try:
            self.box_connections.__delitem__(ASMBox.selected_box)
        except:
            # print("here1")
            pass
        # print(f"box connections is {self.box_connections}")

        if ASMBox.selected_box.text_id is not None:
            self.canvas.delete(ASMBox.selected_box.text_id)

        try:
            if next_selected_box is not None:
                next_selected_box.select_box()
            else:ASMBox.selected_box=None
        except:
            # print("here3")
            pass
        if ASMBox.selected_box is not None:
            x_right_scroll_region = max(window_width+50,min(float(self.canvas['scrollregion'].split(" ")[2]),self.get_the_most_right_box_x()))
            x_left_scroll_region = min(-50,max(float(self.canvas['scrollregion'].split(" ")[0]),self.get_the_most_left_box_x()))
            y_scroll_scroll_region=max(main_canvas.winfo_reqheight(),min(float(self.canvas['scrollregion'].split(" ")[3]),self.get_lowest_box_y()+box_distance))
            self.canvas['scrollregion'] = (x_left_scroll_region, 0, x_right_scroll_region, y_scroll_scroll_region)
        # print(self.box_connections)
    def delete_route(self):
        global route_mode_right
        if route_mode_right.get():
            if ASMBox.selected_box.route_arrows[1]==None:
                messagebox.showinfo("Deletion error","This box doesn't have a right route to be deleted!")
            else:
                self.canvas.delete(ASMBox.selected_box.route_arrows[1])
                self.canvas.delete(ASMBox.selected_box.route_arrows_text_ids[1])
                ASMBox.selected_box.route_arrows[1]=None
                ASMBox.selected_box.route_arrows_text_ids[1]=None
                ASMBox.selected_box.child_boxes[1].parent_boxes.remove(ASMBox.selected_box)
                ASMBox.selected_box.child_arrows[1]=None
                ASMBox.selected_box.child_boxes[1]=None

        else:
            if ASMBox.selected_box.route_arrows[0]==None:
                messagebox.showinfo("Deletion error", "This box doesn't have a left route to be deleted!")
            else:
                self.canvas.delete(ASMBox.selected_box.route_arrows[0])
                self.canvas.delete(ASMBox.selected_box.route_arrows_text_ids[0])
                ASMBox.selected_box.route_arrows[0] = None
                ASMBox.selected_box.route_arrows_text_ids[0] = None
                ASMBox.selected_box.child_boxes[0].parent_boxes.remove(ASMBox.selected_box)
                ASMBox.selected_box.child_arrows[0] = None
                ASMBox.selected_box.child_boxes[0] = None
                self.box_connections[ASMBox.selected_box][0] = None

    def self_loop_happens(self):
        for child in ASMBox.selected_box.child_boxes:
            if child is None:continue
            if child.child_boxes.__contains__(ASMBox.selected_box):
                return True
        return False

    def get_x_middle(self, shape_width):
        global add_mode_right
        if ASMBox.selected_box is None: return window_width / 2 - rectangle_width / 2
        if ASMBox.selected_box.color == 'yellow':
            if add_mode_right.get():
                return float((self.canvas.bbox(ASMBox.selected_box.id)[0] + self.canvas.bbox(ASMBox.selected_box)[2]) / 2) + float(
                    3 * shape_width / 2) + 1
            else:
                return float((self.canvas.bbox(ASMBox.selected_box.id)[0] + self.canvas.bbox(ASMBox.selected_box.id)[2]) / 2) - float(
                    5 * shape_width / 2) + 1
        else:
            return float(self.canvas.bbox(ASMBox.selected_box.id)[0] + 1)

    def add_box_connection(self,add_to_box, added_box,direction="left"):
        # print(f"Add {added_box} to {add_to_box}")
        if None in[added_box,add_to_box]:return
        self.box_connections[add_to_box][0 if direction=="left" else 1]=added_box
        add_to_box.add_child_box(added_box,direction)
        added_box.add_parent_box(add_to_box)


    def dfs_search(self,current_node, visited={}):
        items = []
        if self.box_connections.get(current_node) is None:
            return []
        not_routed_children=list()
        # print(f"current node is {current_node} and its route arrows are {current_node.route_arrows}")
        if current_node.route_arrows[0]==None:
            if current_node.route_arrows[1]==None:
                not_routed_children=self.box_connections[current_node]
            else:
                not_routed_children=[self.box_connections[current_node][0]]
        else:
            if current_node.route_arrows[1]==None:
                not_routed_children = [self.box_connections[current_node][1]]
            else:
                not_routed_children=[]

        for node in not_routed_children:
            # print(f"node in dfs is {node}")
            if node is None :continue
            if visited.get(node) is None:
                visited[node] = 1
                items.append(node)
                items.extend(self.dfs_search(node, visited))
        return items
    def get_lowest_box_y(self):
        return max([box.y for box in self.box_connections])
    def get_the_most_right_box_x(self):
        return max([box.x+box.width+box_distance for box in self.box_connections])
    def get_the_most_left_box_x(self):
        return min([box.x-box_distance for box in self.box_connections])

    def submit_description(self):
        global description_box
        if ASMBox.selected_box is not None:
            # print(ASMBox.selected_box)
            location = self.canvas.bbox(ASMBox.selected_box)
            if ASMBox.selected_box.text_id is not None:
                self.canvas.itemconfig(ASMBox.selected_box.text_id, text='')
            full_text = description_box.get(1.0, 'end-1c')
            count_lines = 1
            shape_text = full_text
            for index, char in enumerate(full_text):
                if char == '\n':
                    count_lines += 1
                if count_lines >= int(description_box_height*scale)-1:
                    shape_text = full_text[:index] + "\n..."
                    break
            text_id = self.canvas.create_text((location[0] + location[2]) / 2, (location[1] + location[3]) / 2,
                                           text=shape_text, tags=f'text{ASMBox.selected_box}',font=default_font)
            self.canvas.tag_bind(f'text{ASMBox.selected_box}', '<Button-1>', lambda *args: self.find_and_select_text_box(full_text))
            ASMBox.selected_box.text_id=text_id
            ASMBox.selected_box.text=full_text
            description_box.delete("1.0", 'end')

    def find_and_select_text_box(self,text):
        for box in self.box_connections:
            if box.text==text:
                box.select_box()
                break
    def zoom_in(self):
        global scale,rectangle_width, rectangle_height, oval_r1, oval_r2,box_distance
        main_canvas.scale('all', 0, 0, 1.25, 1.25)
        scale*=1.25
        rectangle_height *= 1.25
        rectangle_width *= 1.25
        box_distance*=1.25
        oval_r1 *= 1.25
        oval_r2 *= 1.25

        for box in self.box_connections:
            box.y*=1.25
            box.x*=1.25

        y_scroll_region = float(self.canvas['scrollregion'].split(" ")[3])
        x_right_scroll_region = float(self.canvas['scrollregion'].split(" ")[2])
        x_left_scroll_region = float(self.canvas['scrollregion'].split(" ")[0])
        self.canvas['scrollregion'] = (
        x_left_scroll_region * 1.25, 0, x_right_scroll_region * 1.25, y_scroll_region * 1.25)
        self.adjust_texts_with_zoom()
    def zoom_out(self):
        global scale, rectangle_width, rectangle_height, oval_r1, oval_r2,box_distance
        main_canvas.scale('all', 0, 0, 0.8, 0.8)
        scale*=0.8
        rectangle_height *=0.8
        rectangle_width *= 0.8
        box_distance*=0.8
        oval_r1 *= 0.8
        oval_r2 *= 0.8
        for box in self.box_connections:
            box.y*=0.8
            box.x*=0.8

        y_scroll_region = float(self.canvas['scrollregion'].split(" ")[3])
        x_right_scroll_region = float(self.canvas['scrollregion'].split(" ")[2])
        x_left_scroll_region = float(self.canvas['scrollregion'].split(" ")[0])
        self.canvas['scrollregion'] = (x_left_scroll_region * 0.8, 0, x_right_scroll_region * 0.8, y_scroll_region * 0.8)
        self.adjust_texts_with_zoom()
    def adjust_texts_with_zoom(self):
        global scale,description_box_height
        for box in self.box_connections:
            count_lines=1
            shape_text=box.text
            for index, char in enumerate(box.text):
                if char == '\n':
                    count_lines += 1
                if count_lines >= int(description_box_height * scale)-1:
                    shape_text = box.text[:index] + "\n..."
                    break
            self.canvas.itemconfig(box.text_id,text=shape_text)

    def run_ASM_chart(self):
        global all_blocks
        for key in self.box_connections:
            message=f"{key.custom_id} is connected to "
            if self.box_connections[key][0] is not None:
                message+=str(self.box_connections[key][0].custom_id)
            if self.box_connections[key][1] is not None:
                message+=str(self.box_connections[key][1].custom_id)
            # print(message)

        #validate the ASM chart
        possible_error=self.get_ASM_chart_error()
        if possible_error!='':
            messagebox.showinfo("Run error",possible_error)
        else:
            all_blocks={}
            for box in self.box_connections:
                block=Block()
                if box.type=='state':
                    block.block_type='A'
                elif box.type=='decision':
                    block.block_type='B'
                else:
                    block.block_type='C'
                block.next_block=self.box_connections[box][0].custom_id - 1
                if self.box_connections[box][1] != None:
                    block.next_next_block=self.box_connections[box][1].custom_id - 1
                block.all_lines=box.text.strip().split("\n")
                all_blocks[box.custom_id - 1] = block
                # print(block.block_type, block.all_lines)
            # print(all_blocks)
            self.preprocess()
            self.generate_verilog_code_for_blocks()
            self.generate_verilog_code_for_total_module()
            self.generate_verilog_code_for_data_path()
            self.generate_verilog_code_for_control_unit()
            self.generate_verilog_code_for_main_program()
            messagebox.showinfo("Run","The ASM chart ran successfully and the verilog output is ready!")
    def get_ASM_chart_error(self):
        error1="A decision box should be connected on both sides"
        error2= "A condition box must follow a decision box"
        error3="All decision and condition boxes should have a text!"
        for box in self.box_connections:
            if box.type=='decision':
                if None in self.box_connections[box]:
                    return error1
            elif box.type=='condition':
                for parent in box.parent_boxes:
                    if parent.type!='decision':
                        return error2
            if box.type!='state':
                if box.text=='':
                    return error3
        return ''

    def preprocess(self):
        global all_blocks
        # for i in range(len(all_blocks)):
        for i in all_blocks:
            block = all_blocks[i]
            # print(block.all_lines)
            if not block.all_lines or block.all_lines[0]=='':
                # print(f"{block} is empty")
                block.empty = True

    def generate_write_symbols_of_block(sefl,block_index):
        global all_blocks
        block = all_blocks[block_index]
        # print("generate_write_symbols_of_block")
        # print(block)
        if block.block_type == 'B':
            return set([])
        lines = block.all_lines
        all_write_symbols = []
        # print("lines = ", lines)
        for line in lines:
            # print("line = ", line)
            x = 0
            y = line.split()
            while '#' in y[x]:
                x = x + 1
            first_input = y[x]
            all_write_symbols.append(first_input)
        all_write_symbols = set(all_write_symbols)
        return all_write_symbols

    def generate_not_necessary_write_symbols_of_block(self,block_index):
        global all_blocks
        block = all_blocks[block_index]
        lines = block.all_lines
        all_write_symbols = []
        # print("generate_not_necessary_write_symbols_of_block")
        # print(block)
        for line in lines:
            if block.block_type == 'B':
                all_input = line.split()[0:]
            else:
                x = 0
                y = line.split()
                while y[x] != '=' and y[x] != '<=':
                    x = x + 1
                all_input = y[x:]
            # print("all_input = ", all_input)
            for one_input in all_input:
                if one_input.isalnum() and not one_input.isnumeric():
                    all_write_symbols.append(one_input)
        all_write_symbols = set(all_write_symbols)
        return all_write_symbols

    def generate_verilog_code_for_total_module(self):
        global all_blocks
        f = open("total_module.v", "a")
        f.write("module total_module")
        all_inputs = set()
        all_regs = set()
        all_everything = set()
        one_liner = ""
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None:continue
            if not block.empty and (block.block_type == 'A' or block.block_type == 'C'):
                # f.write("Now the file has more content!")
                one_liner += ("Enable" + str(block_index + 1) + ", ")
                write_symbol = self.generate_write_symbols_of_block(block_index)
                not_necessary_write_symbol = self.generate_not_necessary_write_symbols_of_block(block_index)
                input_symbol = set()
                for a_not_necessary_write_symbol in not_necessary_write_symbol:
                    if a_not_necessary_write_symbol not in write_symbol:
                        input_symbol.add(a_not_necessary_write_symbol)
                all_inputs = all_inputs | input_symbol
                all_regs = all_regs | write_symbol
        all_inputs = all_inputs - all_regs
        for symbol in all_inputs | all_regs:
            one_liner += symbol
            one_liner += ", "
            # one_liner = one_liner[0:-2]

        f.write("(" + one_liner + "clk);\n")
        for a_write_symbol in all_regs:
            f.write("output reg[31:0] " + a_write_symbol + ";\n")
        for a_write_symbol in all_inputs:
            f.write("input [31:0] " + a_write_symbol + ";\n")
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None: continue
            if not block.empty and (block.block_type == 'A' or block.block_type == 'C'):
                f.write("input Enable" + str(block_index + 1) + ";\n")
        f.write("input clk;\n")
        f.write("always @(posedge clk) begin\n")
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None: continue
            if not block.empty and (block.block_type == 'A' or block.block_type == 'C'):
                f.write("if (Enable" + str(block_index + 1) + ") begin\n")
                for line in block.all_lines:
                    f.write(line + ";\n")
                f.write("end\n")
        f.write("end\nendmodule")
        f.close()

    def generate_verilog_code_for_blocks(self):
        global all_blocks
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None: continue
            if not block.empty and block.block_type == 'B':
                f = open("module" + str(block_index + 1) + ".v", "a")
                # f.write("Now the file has more content!")
                f.write("module module" + str(block_index + 1))
                write_symbol = self.generate_write_symbols_of_block(block_index)
                not_necessary_write_symbol = self.generate_not_necessary_write_symbols_of_block(block_index)
                all_symbols = set(write_symbol | not_necessary_write_symbol)
                # print("Attention! Writing block", block_index)
                # print("write_symbol = ", write_symbol)
                # print("not_necessary_write_symbol = ", not_necessary_write_symbol)
                # print("all_symbols = ", all_symbols)
                one_liner = ""
                for symbol in all_symbols:
                    one_liner += symbol
                    one_liner += ", "
                    # one_liner = one_liner[0:-2]

                f.write("(" + one_liner + "output" + str(block_index + 1) + ");\n")
                for symbol in all_symbols:
                    f.write("input [31:0] " + symbol + ";\n")
                f.write("output reg [31:0] output" + str(block_index + 1) + ";\n")
                f.write("always @(")
                t = 0
                for symbol in all_symbols:
                    t = t + 1
                    if t != len(all_symbols):
                        f.write(symbol + ", ")
                    else:
                        f.write(symbol)
                f.write(")\nbegin\n")
                for line in block.all_lines:
                    f.write("if (" + line + ") begin\noutput" + str(
                        block_index + 1) + " = 1;\nend else begin\noutput" + str(
                        block_index + 1) + " = 0; end\n")
                f.write("end\nendmodule")
                f.close()

    def generate_verilog_code_for_data_path(self):
        global all_blocks
        f = open("data_path.v", "a")
        all_inputs = set()
        all_wires = set()
        all_outputs = set()
        unknown_inputs = set()
        unknown_outputs = set()
        unknown_wires = set()
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None: continue
            if not block.empty and block.block_type == 'B':
                # write_symbol = generate_write_symbols_of_block(block_index)
                not_necessary_write_symbol = self.generate_not_necessary_write_symbols_of_block(block_index)
                input_symbol = not_necessary_write_symbol
                unknown_inputs = unknown_inputs | input_symbol
        all_inputs1 = set()
        all_regs = set()
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None: continue
            if not block.empty and (block.block_type == 'A' or block.block_type == 'C'):
                # f.write("Now the file has more content!")
                write_symbol = self.generate_write_symbols_of_block(block_index)
                not_necessary_write_symbol = self.generate_not_necessary_write_symbols_of_block(block_index)
                input_symbol = set()
                for a_not_necessary_write_symbol in not_necessary_write_symbol:
                    if a_not_necessary_write_symbol not in write_symbol:
                        input_symbol.add(a_not_necessary_write_symbol)
                all_inputs1 = all_inputs1 | input_symbol
                all_regs = all_regs | write_symbol
        all_inputs1 = all_inputs1 - all_regs

        all_wires = unknown_wires | (all_regs & unknown_inputs)
        all_outputs = all_regs - unknown_inputs
        all_inputs = (unknown_inputs - all_regs) | all_inputs1

        f.write("module data_path(")
        one_liner = ""
        for symbol in all_inputs | all_outputs:
            one_liner += symbol
            one_liner += ", "
        f.write(one_liner)
        one_liner = ""
        for block_index in all_blocks:
            if all_blocks[block_index] is None:continue
            if not all_blocks[block_index].empty:
                if all_blocks[block_index].block_type != 'B':
                    one_liner += "Enable"
                    one_liner += str(block_index + 1)
                    one_liner += ", "
                else:
                    one_liner += "output"
                    one_liner += str(block_index + 1)
                    one_liner += ", "
        f.write(one_liner + "clk);\n")
        # 1st line is for module (...);
        one_liner = ""
        counter=0
        for block_index in all_blocks:
            if all_blocks[block_index] is None:continue
            if not all_blocks[block_index].empty:
                if all_blocks[block_index].block_type != 'B':
                    one_liner += "Enable"
                    one_liner += str(block_index + 1)
                    if counter!= len(all_blocks) - 1:
                        one_liner += ", "
            counter+=1
        f.write("input " + one_liner[0:] + ";\n")
        # 2nd line is for input of Enables of A, C blocks

        one_liner = ""
        for block_index in all_blocks:
            if all_blocks[block_index] is None:continue
            if all_blocks[block_index].block_type == 'B':
                one_liner += "output"
                one_liner += str(block_index + 1)
                one_liner += ", "
        f.write("output [31:0] " + one_liner[0:-2] + ";\n")
        # 3rd line is for output of B Blocks

        f.write("input clk;\n")
        # 4th line is for clock

        for one_input_wire in all_inputs:
            f.write("input [31:0] " + one_input_wire + ";\n")

        for one_output_wire in all_outputs:
            f.write("output [31:0] " + one_output_wire + ";\n")

        for one_wire in all_wires:
            f.write("wire [31:0] " + one_wire + ";\n")

        for file_index in all_blocks:
            if all_blocks[file_index] is None:continue
            if not all_blocks[file_index].empty and all_blocks[file_index].block_type == 'B':
                with open('module' + str(file_index + 1) + ".v") as g:
                    first_line = g.readline()
                    first_line = "module" + str(file_index + 1) + " create_module" + first_line[13:-4] + str(
                        file_index + 1) + ");\n"  # DOUBBBBBBBBBBBBBBBT
                    f.write(first_line)
        with open("total_module.v") as g:
            first_line = g.readline()
            first_line = "total_module total_module1" + first_line[19:-2] + ";\n"  # DOUBBBBBBBBBBBBBBBT
            f.write(first_line)
        f.write("endmodule")
        f.close()

    def return_strings_for_activating_enables(self,block_index, dirty):
        global all_blocks
        block = all_blocks[block_index]
        if dirty[block_index]:
            return "begin n_state = " + str(block_index + 1) + "; end\n"
        dirty[block_index] = True
        if all_blocks[block.next_block].block_type != 'A':
            if block.block_type == 'A':
                if not block.empty:
                    return "begin Enable" + str(
                        block_index + 1) + " = 1; end\n" + self.return_strings_for_activating_enables(block.next_block,
                                                                                                 dirty)
                else:
                    return self.return_strings_for_activating_enables(block.next_block, dirty)
            elif block.block_type == 'B':
                return "if (output" + str(block_index + 1) + " == 1) begin\n" + self.return_strings_for_activating_enables(
                    block.next_block, dirty) + \
                       "end else begin\n" + self.return_strings_for_activating_enables(block.next_next_block,
                                                                                  dirty) + "end\n"
            elif block.block_type == 'C':
                if not block.empty:
                    return "begin Enable" + str(
                        block_index + 1) + " = 1; end\n" + self.return_strings_for_activating_enables(block.next_block,
                                                                                                 dirty)
                else:
                    return self.return_strings_for_activating_enables(block.next_block, dirty)
        elif all_blocks[block.next_block].block_type == 'A':
            if block.block_type == 'A':
                if not block.empty:
                    return "begin Enable" + str(block_index + 1) + " = 1; end\n" + "begin n_state = " + str(
                        block.next_block + 1) + "; end\n"
                else:
                    return "begin n_state = " + str(block.next_block + 1) + "; end\n"
            elif block.block_type == 'B':
                if all_blocks[block.next_next_block].block_type == 'A':
                    return "if (output" + str(block_index + 1) + " == 1) begin\n" + "begin n_state = " + str(
                        block.next_block + 1) + "; end\n" \
                           + "end else begin\n" + "begin n_state = " + str(block.next_next_block + 1) + "; end\nend\n"
                else:
                    return "if (output" + str(block_index + 1) + " == 1) begin\n" + "begin n_state = " + str(
                        block.next_block + 1) + "; end\n" \
                           + "end else begin\n" + self.return_strings_for_activating_enables(block.next_next_block,
                                                                                        dirty) + "end\n"
            elif block.block_type == 'C':
                if not block.empty:
                    return "begin Enable" + str(block_index + 1) + " = 1; end\n" + "begin n_state = " + str(
                        block.next_block + 1) + "; end\n"
                else:
                    return "begin n_state = " + str(block.next_block + 1) + "; end\n"

    def generate_verilog_code_for_control_unit(self):
        global all_blocks
        data_path = open('data_path.v', 'r')
        lines = data_path.readlines()
        first_line = lines[1][6:-2]  # Enables which are outputs for control unit
        second_line = lines[2][14:-2]  # outputs of B blocks that are inputs for control unit
        f = open("control_unit.v", "a")
        if first_line != " " and second_line != "":
            f.write("module control_unit(" + first_line + ", " + second_line + ", clk, rst);\n")
        else:
            f.write("module control_unit(" + first_line + second_line + ", clk, rst);\n")
        f.write("input [31:0] " + second_line + ";\n")
        f.write("output reg " + first_line + ";\n")
        f.write("input clk, rst;\n")
        continue_reading = False
        keep_reading = True
        # for line in lines[2:]:
        #     if line.startswith("output [31:0]") and keep_reading:
        #         f.write("input [31:0] "+line[17:])
        #         continue_reading = True
        #     else:
        #         if continue_reading:
        #             keep_reading = False
        #             continue_reading = False
        f.write("integer p_state, n_state;\n\n")
        f.write(
            "always @ (posedge clk)\nbegin\nif (rst == 1'b0) begin p_state = 1; end\nelse begin p_state = n_state; end\nend\n")
        f.write("\n")
        f.write("always @(p_state, " + second_line + ")\nbegin\n")
        f.write("begin\n")
        for block_index in all_blocks:
            if all_blocks[block_index] is None:
                continue
            if not all_blocks[block_index].empty:
                if all_blocks[block_index].block_type != 'B':
                    f.write("Enable" + str(block_index + 1) + " = 0;\n")
        f.write("end\n")
        f.write("case(p_state)\n")
        for block_index in all_blocks:
            block = all_blocks[block_index]
            if block is None:continue
            if block.block_type == 'A':
                f.write(str(block_index + 1) + ":\n")
                f.write("begin\n")
                f.write(self.return_strings_for_activating_enables(block_index, [False] * len(all_blocks)))
                f.write("end\n")
        f.write("endcase\nend\nendmodule")
        f.close()

    def generate_verilog_code_for_main_program(self):
        global all_blocks
        data_path = open('data_path.v', 'r')
        lines = data_path.readlines()
        f = open("main_program.v", "a")
        f.write("module main_program")
        continue_reading = True
        list_of_input_output = ''
        for line in lines[4:]:
            # print(line)
            if continue_reading and line.startswith("input [31:0]"):
                list_of_input_output += line[13:-2]
                list_of_input_output += ", "
                # print(list_of_input_output)
            elif continue_reading and line.startswith("output [31:0]"):
                list_of_input_output += line[14:-2]
                list_of_input_output += ", "
                # print(list_of_input_output)
            elif continue_reading:
                continue_reading = False
                # print(list_of_input_output)
                list_of_input_output = list_of_input_output[:-2]
                # print(list_of_input_output)
        f.write("(" + list_of_input_output + ", clk, rst);\n")
        first_line = lines[1][6:-2]  # Enables which are outputs for control unit
        second_line = lines[2][14:-2]  # outputs of B blocks that are inputs for control unit
        f.write("wire " + first_line + ";\n")
        f.write("wire [31:0] " + second_line + ";\n")
        # if first_line != "" and second_line != "":
        #    f.write("wire [31:0] " + first_line + ", " + second_line + ";\n")
        # else:
        #    f.write("wire [31:0] " + first_line + second_line + ";\n")
        f.write("input clk, rst;\n")
        continue_reading = True
        for line in lines[4:]:
            if continue_reading and line.startswith("input [31:0]"):
                f.write("input [31:0] " + line[13:-2] + ";\n")
            elif continue_reading and line.startswith("output [31:0]"):
                f.write("output [31:0] " + line[14:-2] + ";\n")
            else:
                continue_reading = False
        first_line = lines[0][16:-2]
        f.write("data_path dp" + first_line + ";\n")
        control_unit = open('control_unit.v', 'r')
        lines = control_unit.readlines()
        first_line = lines[0][19:-2]  # control unit inputs
        f.write("control_unit cu" + first_line + ";\n")
        f.write("endmodule")
        f.close()
    # print("Welcome to Python to Verilog Conversion Program!")
    # print("print \"Start\" to start the program.")
    # print("")
    # continue_program = True
    # input_state = 1
    # input_step_within_state = 0
    # block_number = 1




class ASMBox:
    id_last_box = 0
    selected_box=None

    def __init__(self, graph: ASMGraph, _type):
        x_middle = graph.get_x_middle(rectangle_width)
        # print(f"selected box is {ASMBox.selected_box}")
        if ASMBox.selected_box is not None:
            y_selected_box = ASMBox.selected_box.y
        else:
            y_selected_box = 30
        ASMBox.id_last_box += 1
        self.type=_type
        self.graph=graph
        if _type == "state":
            self.id = graph.canvas.create_rectangle(x_middle, y_selected_box + box_distance,
                                                     x_middle + rectangle_width,
                                                     y_selected_box + box_distance + rectangle_height,
                                                     fill='chartreuse',
                                                     tags=f'box{ASMBox.id_last_box}')
            self.color='chartreuse'
            self.height = rectangle_height
            self.width = rectangle_width
        elif _type == "condition":
            self.id = graph.canvas.create_oval(x_middle, y_selected_box + box_distance, x_middle + oval_r1,
                                                y_selected_box + box_distance + oval_r2, fill='orange',
                                                tags=f'box{ASMBox.id_last_box}')
            self.color='orange'
            self.height = oval_r2
            self.width = oval_r1
        else:
            self.id = graph.canvas.create_polygon(x_middle, y_selected_box + box_distance + rectangle_height / 2,
                                                   x_middle + rectangle_width / 2,
                                                   y_selected_box + box_distance, x_middle + rectangle_width,
                                                   y_selected_box + box_distance + rectangle_height / 2,
                                                   x_middle + rectangle_width / 2,
                                                   y_selected_box + box_distance + rectangle_height, fill='yellow',
                                                   tags=f'box{ASMBox.id_last_box}')
            self.color='yellow'
            self.height = rectangle_height
            self.width = rectangle_width

        self.custom_id=ASMBox.id_last_box
        self.x = x_middle
        self.y = 30+self.height+box_distance if ASMBox.selected_box is None else ASMBox.selected_box.y+self.height+box_distance

        self.number_text_id = self.graph.canvas.create_text(self.x+10,self.y-self.height+10,text=str(ASMBox.id_last_box),font=default_font,fill='red')
        self.text = ""
        self.text_id = None

        self.graph.canvas.tag_bind(f"box{ASMBox.id_last_box}", "<Button-1>", lambda *args: self.select_box())

        self.child_arrows = [None, None]
        self.parent_arrow = None
        self.child_boxes=[None,None]
        self.parent_boxes=[]

        # self.is_left_rooted = False
        # self.is_right_rooted=False
        #
        self.route_arrows=[None, None]
        self.route_arrows_text_ids=[None,None]

        graph.box_connections[self]=[None,None]

    def add_text(self, text, text_id):
        self.text = text
        self.text_id = text_id

    def remove_text(self):
        self.text = ""
        self.text_id = None

    def set_child_arrow(self, arrow, direction="left"):
        if direction == "left":
            self.child_arrows[0] = arrow
        else:
            self.child_arrows[1] = arrow

    def set_parent_arrow(self, arrow):
        self.parent_arrow=arrow

    def add_child_box(self, box, direction="left"):
        if direction == "left":
            self.child_boxes[0] = box
        else:
            self.child_boxes[1] = box

    def remove_child_box(self, box):
        self.child_boxes.remove(box)

    def add_parent_box(self, box):
        self.parent_boxes.append(box)

    def remove_parent_box(self, box):
        self.parent_boxes.remove(box)

    def change_color(self,to_select_color=True):
        self.graph.canvas.itemconfig(self.id,fill="purple" if to_select_color else self.color)

    def select_box(self):
        global description_box, delete_box_button, add_right_button,add_left_button,route_button,right_route_button,left_route_button,route_mode,delete_route_button
        # print(f"{self} selected!!")
        if ASMBox.selected_box is not None:
            if route_mode.get():
                self.handle_routing()
            ASMBox.selected_box.change_color(False)
            description_box.delete('1.0', 'end')
        self.change_color(True)
        ASMBox.selected_box = self

        if ASMBox.selected_box.type=="decision":
            # print(f"selected child boxes are {ASMBox.selected_box.child_boxes}")
            if ASMBox.selected_box.child_boxes!=[None,None]:
                switch_button(delete_box_button,False)
            else:
                switch_button(delete_box_button,True)
        else:switch_button(delete_box_button, True)
        route_button['state']='active'
        if ASMBox.selected_box.type=="decision":
            if route_mode.get():
                right_route_button['state']='active'
                left_route_button['state']='active'
            else:
                add_right_button['state'] = 'active'
                add_left_button['state'] = 'active'
        else:
            right_route_button['state'] = 'disable'
            left_route_button['state'] = 'disable'
            add_right_button['state'] = 'disable'
            add_left_button['state'] = 'disable'

        if ASMBox.selected_box.text_id is not None:
            description_box.insert(tk.END,ASMBox.selected_box.text)



    def handle_routing(self):
        global route_mode,route_mode_right
        route_source=ASMBox.selected_box
        route_destination=self
        # print(f"route source is {route_source} and route destination is {route_destination}")
        #check errors
        if route_source==route_destination:
            messagebox.showinfo("Error in routing","You can't route a box to itself!")
            return
        if route_source.type=='decision' and (route_source.child_boxes[0]!=None and not route_mode_right.get() or \
                route_source.child_boxes[1]!=None and route_mode_right.get())or route_source.type!='decision' and route_source.child_boxes[0] is not None:
            messagebox.showinfo("Error in routing","This box is already connected to some boxes!")
            return

        if route_source.type=='decision' and route_mode_right.get():
            route_source.child_arrows[1]=route_destination.parent_arrow
            route_source.child_boxes[1]=route_destination
            route_destination.add_parent_box(route_source)
            self.graph.box_connections[route_source][1] = route_destination
            # route_source.is_right_rooted=True
            route_source.route_arrows[1]=self.graph.canvas.create_line(route_source.x+route_source.width,route_source.y-route_source.height/2,route_source.x+route_source.width+box_distance,
                                                                       route_source.y-route_source.height/2,arrow=tk.LAST,fill="red")
            route_source.route_arrows_text_ids[1] = self.graph.canvas.create_text(route_source.x + route_source.width+box_distance,
                                                                                  route_source.y - route_source.height / 2 - 10,
                                                                                  text=str(route_destination.custom_id),
                                                                                  font=default_font, fill="red")
        else:
            route_source.child_arrows[0] = route_destination.parent_arrow
            route_source.child_boxes[0] = route_destination
            route_destination.add_parent_box(route_source)
            self.graph.box_connections[route_source][0]=route_destination
            route_source.route_arrows[0]=self.graph.canvas.create_line(route_source.x,route_source.y-route_source.height/2,route_source.x-box_distance,
                                                                       route_source.y-route_source.height/2,arrow=tk.LAST,fill="red")
            route_source.route_arrows_text_ids[0]=self.graph.canvas.create_text(route_source.x-box_distance,route_source.y-route_source.height/2-10,
                                                                                text=str(route_destination.custom_id),font=default_font,fill="red")


        # print(self.graph.box_connections)




    def __repr__(self):
        return str(self.id)

def switch_button(button: Button,to_on:bool):
    if to_on:
        button['state'] = ACTIVE
        button['bg'] = 'chartreuse'
    else:
        button['state'] = DISABLED
        button['bg'] = 'red'

def on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def clear_all():
    global graph
    main_canvas.delete('all')
    ASMBox.selected_box=None
    ASMBox.id_last_box=0
    graph=ASMGraph(main_canvas)
    switch_button(delete_box_button,False)
    main_canvas['scrollregion']=(-50,0,window_width+50,main_canvas.winfo_reqheight())

def select_route_button(right_route_button,left_route_button,route_button,add_mode_button,delete_route_button):
    route_button.select()
    add_mode_button.deselect()
    add_right_button['state'] = 'disable'
    add_left_button['state'] = 'disable'
    if ASMBox.selected_box is not None and ASMBox.selected_box.type=='decision':
        right_route_button['state']='active'
        left_route_button['state']='active'
    else:
        right_route_button['state']='disable'
        left_route_button['state']='disable'
    if ASMBox.selected_box.route_arrows != [None, None]:
        switch_button(delete_route_button,True)

def select_add_shape_button(right_route_button, left_route_button, route_button,add_mode_button):
    add_mode_button.select()
    route_button.deselect()
    right_route_button['state'] = 'disable'
    left_route_button['state'] = 'disable'
    if ASMBox.selected_box is not None and ASMBox.selected_box.type=='decision':
        add_right_button['state']='active'
        add_left_button['state']='active'
    else:
        add_right_button['state']='disable'
        add_left_button['state']='disable'

class GUI:
    def __init__(self):
        global main_canvas,description_box,run_button,delete_box_button,add_shape_button,state_box_icon,decision_box_icon,\
            condition_box_icon,route_button,right_route_button,left_route_button,\
            add_right_button,add_left_button,route_mode,route_mode_right,add_mode,add_mode_right,delete_route_button,graph
        self.root=Tk()
        self.root.title('ASM chart builder')
        self.root.resizable(width=0,height=0)

        self.root.geometry(f'{window_width}x{window_height}')
        x_left = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        y_top=0
        self.root.geometry(f'+{x_left}+{y_top}')
        self.root.config(bg='black')

        main_frame = LabelFrame(self.root, bg='black', padx=0, pady=0)
        main_frame.pack(expand=True,fill=BOTH)
        main_canvas = Canvas(main_frame, height=window_height - side_canvas_height, width=side_canvas_width, bg='grey')
        sb_vertical = Scrollbar(main_frame, orient=VERTICAL)
        sb_vertical.config(command=main_canvas.yview)
        sb_vertical.pack(side=RIGHT, fill=X)

        sb_horizontal = Scrollbar(main_frame, orient=HORIZONTAL)
        sb_horizontal.config(command=main_canvas.xview)
        sb_horizontal.pack(side=BOTTOM, fill=Y)

        main_canvas.config(yscrollcommand=sb_vertical.set,xscrollcommand=sb_horizontal.set)

        main_canvas.bind_all("<MouseWheel>", lambda *args:on_mousewheel(args[0]))
        main_canvas['scrollregion']=(-50,0,window_width+50,main_canvas.winfo_reqheight())
        main_canvas.pack(side=LEFT,expand=True,fill=BOTH)
        graph=ASMGraph(main_canvas)
        side_frame=LabelFrame(self.root,bg='gray',padx=0,pady=0)
        side_frame.pack()
        side_canvas=Canvas(side_frame,height=side_canvas_height,width=side_canvas_width,bg='grey')
        x_offset=20
        y_offset=20
        state_box_icon=side_canvas.create_rectangle(x_offset,y_offset,x_offset+rectangle_width,y_offset+rectangle_height
                                                    ,fill='chartreuse',activefill='purple',tags='state_box_icon')
        condition_box_icon=side_canvas.create_oval(2*x_offset+rectangle_width,y_offset,2*x_offset+rectangle_width+oval_r1,
                                                   y_offset+oval_r2,fill='orange',activefill='purple',tags='condition_box_icon')
        decision_box_icon=side_canvas.create_polygon(3*x_offset+oval_r1+rectangle_width,y_offset+rectangle_height/2,
                                                     3*x_offset+oval_r1+3*rectangle_width/2,y_offset,
                                                     3*x_offset+oval_r1+2*rectangle_width,y_offset+rectangle_height/2,
                                                     3*x_offset+oval_r1+3*rectangle_width/2,y_offset+rectangle_height,
                                                     fill='yellow',activefill='purple',tags='decision_box_icon')
        side_canvas.tag_bind('state_box_icon',"<Button-1>",lambda *args:graph.add_box("state"))
        side_canvas.tag_bind('condition_box_icon', "<Button-1>",lambda *args:graph.add_box("condition"))
        side_canvas.tag_bind('decision_box_icon', "<Button-1>", lambda *args:graph.add_box("decision"))
        side_canvas.pack()


        description_label=Label(side_frame,text='Type the description in the box below:',fg='cyan',bg='grey',font=default_font)
        description_label.place(
            x=9 * x_offset + oval_r1 + 2 * rectangle_width, y=y_offset/10
        )
        description_box=Text(side_frame,height=description_box_height,width=description_box_width,bg='light cyan',font=default_font,
                             wrap='word')
        description_box.place(
            x=10 * x_offset + oval_r1 + 2 * rectangle_width, y=y_offset
        )
        submit_button=Button(side_frame,height=button_height,width=button_width,bg='chartreuse',text='Submit',
                             command=lambda *args:graph.submit_description(),font=default_font,activebackground='purple')
        submit_button.place(
            x=13 * x_offset + oval_r1 + 2 * rectangle_width, y=5*y_offset
        )
        delete_box_button=Button(side_frame,height=button_height,width=2*button_width,bg='chartreuse',text='Delete Box',
                             command=lambda *args:graph.delete_box(),font=default_font,activebackground='chartreuse')
        delete_box_button.place(
            x=x_offset, y=5 * y_offset
        )
        delete_route_button=Button(side_frame,height=button_height,width=2*button_width,bg='chartreuse',text='Delete Route',
                                   command=lambda *args:graph.delete_route(),font=default_font,activebackground='chartreuse')
        delete_route_button.place(
            x=delete_box_button.winfo_reqwidth()+2*x_offset,y=5*y_offset
        )

        run_button=Button(side_frame, height=button_height, width=button_width, bg='chartreuse', text='Run', command=lambda *args: graph.run_ASM_chart(),
                          font=default_font, activebackground='purple')
        run_button.place(
            x=delete_box_button.winfo_reqwidth()+delete_route_button.winfo_reqwidth()+5*x_offset, y=5 * y_offset
        )
        clear_all_button = Button(side_frame, height=button_height, width=3*button_width, bg='chartreuse', text='Clear ASM Chart',
                                  command=lambda *args:clear_all(),font=default_font,activebackground='purple')
        clear_all_button.place(
            x=delete_box_button.winfo_reqwidth()+delete_route_button.winfo_reqwidth()+run_button.winfo_reqwidth()+6*x_offset, y=5 * y_offset
        )
        add_mode = tk.BooleanVar()
        add_mode_right=tk.BooleanVar()
        route_mode = tk.BooleanVar()
        route_mode_right=tk.BooleanVar()
        add_shape_button=Checkbutton(side_frame, text='Add Box', bg='grey', variable=add_mode, onvalue=True, offvalue=False,
                                     font=default_font,command=lambda *args: select_add_shape_button(right_route_button,
                                                                                     left_route_button, route_button,add_shape_button))
        add_shape_button.place(
            x=4*x_offset+3*rectangle_width,y=y_offset/2
        )
        add_right_button = Checkbutton(side_frame, text='Right', bg='grey', variable=add_mode_right, onvalue=True,
                                       offvalue=False,font=default_font)
        add_right_button.place(
            x=5 * x_offset + 3 * rectangle_width, y=3*y_offset/2
        )
        add_left_button = Checkbutton(side_frame, text='Left', bg='grey', variable=add_mode_right, onvalue=False,
                                       offvalue=True,font=default_font)
        add_left_button.place(
            x=5 * x_offset + 3 * rectangle_width, y=5*y_offset/2
        )
        route_button =tk. Checkbutton(side_frame, text='Add Route',bg='grey',variable=route_mode,onvalue=True,offvalue=False,font=default_font,
                                    command=lambda *args:select_route_button(right_route_button,left_route_button,route_button,add_shape_button,delete_route_button))
        route_button.place(
            x=4 * x_offset + 3 * rectangle_width, y=7 * y_offset/2
        )
        right_route_button = tk.Checkbutton(side_frame, text='Right', bg='grey',variable=route_mode_right,onvalue=True,offvalue=False,font=default_font)
        right_route_button.place(
            x=5 * x_offset + 3 * rectangle_width, y=9 * y_offset/2
        )
        left_route_button = tk.Checkbutton(side_frame, text='Left', bg='grey',variable=route_mode_right,onvalue=False,offvalue=True,font=default_font)
        left_route_button.place(
            x=5 * x_offset + 3 * rectangle_width, y=11 * y_offset/2
        )
        route_button['state']='disable'
        right_route_button['state']='disable'
        left_route_button['state']='disable'
        add_right_button['state']='disable'
        add_left_button['state']='disable'

        zoom_out_button=Button(main_frame,text='-',bg='white',command=graph.zoom_out,font=default_font)
        zoom_out_button.place(x=window_width-20,y=window_height-side_canvas_height-40)
        zoom_in_button=Button(main_frame,text='+',bg='white',command=graph.zoom_in,font=default_font)
        zoom_in_button.place(x=window_width-20,y=window_height-side_canvas_height-20)
        # switch_button(run_button,False)
        switch_button(delete_box_button,False)
        switch_button(delete_route_button,False)

    def start(self):
        add_shape_button.select()
        self.root.mainloop()

if __name__ == '__main__':
    app=GUI()
    app.start()
