

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        epsilon = 1e-2
        return abs(self.x - other.x) < epsilon and abs(self.y - other.y) < epsilon

    def __hash__(self):
        # Float hash may cause hash collision
        return hash((round(self.x, 2), round(self.y, 2)))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class LaneMarker:
    def __init__(self, direction=None, start_point=None, end_point=None):
        self.direction = direction
        self.start_point = start_point
        self.end_point = end_point

    def __eq__(self, other):
        return self.direction == other.direction and \
               self.start_point == other.start_point and \
               self.end_point == other.end_point

    def __hash__(self):
        return hash((self.direction, self.start_point, self.end_point))

    def __repr__(self):
        return f"LaneMarker({self.direction}, {self.start_point}, {self.end_point})"


class LaneManager:
    def __init__(self):
        self.marker_to_id = {}
        self.id_to_marker = {}
        # self.lanes = {}

    def add_lane(self, lane_id, lane_marker):
        if lane_marker in self.marker_to_id:
            print(f"Lane marker {self.marker_to_id[lane_marker]}: {lane_marker} already exists, new lane id: {lane_id}")
        if lane_id in self.id_to_marker:
            print(f"Lane marker {lane_id}: {self.id_to_marker[lane_id]} already exists")
        self.marker_to_id[lane_marker] = lane_id
        self.id_to_marker[lane_id] = lane_marker
        # self.lanes[lane_id] = pb_lane

    def __len__(self):
        return len(self.marker_to_id)

    def get_lane_id(self, lane_marker):
        if lane_marker not in self.marker_to_id:
            return ""
        return self.marker_to_id[lane_marker]

    def get_lane_marker(self, lane_id):
        return self.id_to_marker[lane_id]

    @staticmethod
    def create_lane_marker(pb_lane):
        center_segment = pb_lane.central_curve.segment[0].line_segment
        point_size = len(center_segment.point)

        start_point_pb = center_segment.point[0]
        end_point_pb = center_segment.point[point_size - 1]

        start_point = Point(start_point_pb.x, start_point_pb.y)
        end_point = Point(end_point_pb.x, end_point_pb.y)

        dx = end_point.x - start_point.x
        dy = end_point.y - start_point.y

        threshold = 0.05
        if abs(dx) < threshold:
            if dy > threshold:
                direction = "bottom_to_top"
            elif dy < -threshold:
                direction = "top_to_bottom"
            else:
                raise ValueError(f"Invalid lane direction: {pb_lane}")

        elif abs(dy) < threshold:
            if dx > threshold:
                direction = "left_to_right"
            elif dx < -threshold:
                direction = "right_to_left"
            else:
                raise ValueError(f"Invalid lane direction: {pb_lane}")

        else:
            direction = "turn"

        return LaneMarker(direction, start_point, end_point)


if __name__ == "__main__":
    # add a test with little point error
    point1 = Point(1, 2)
    point2 = Point(11, 2)
    point3 = Point(5, 2)
    point4 = Point(15.001, 2.001)
    lane_marker1 = LaneMarker("left_to_right", point1, point2)
    lane_marker2 = LaneMarker("left_to_right", point3, point4)
    lane_manager = LaneManager()
    lane_manager.add_lane("lane1", lane_marker1, None)
    lane_manager.add_lane("lane2", lane_marker2, None)
    # print(len(lane_manager))

    point5 = Point(5, 2)
    point6 = Point(15, 2)
    lane_marker3 = LaneMarker("left_to_right", point5, point6)
    print(lane_manager.get_lane_id(lane_marker3))

