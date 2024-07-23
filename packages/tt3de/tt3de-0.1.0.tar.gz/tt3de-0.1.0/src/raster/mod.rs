use nalgebra_glm::{Real, TVec2};
use primitivbuffer::{PointInfo, PrimitivReferences, PrimitiveBuffer, PrimitiveElements};
use pyo3::{pyfunction, PyRefMut, Python};

use crate::{
    drawbuffer::{drawbuffer::DrawBuffer, AbigDrawing},
    primitivbuffer::*,
    vertexbuffer::{VertexBuffer, VertexBufferPy},
};

pub mod raster_line_row;
use raster_line_row::*;
pub mod raster_line_columns;
use raster_line_columns::*;
pub mod raster_line;
use raster_line::*;

pub mod raster_triangle;
use raster_triangle::*;

pub mod raster_point;
use raster_point::*;

pub mod raster_triangle_tomato;
use raster_triangle_tomato::*;

//  calculating min/max of multiple values;
fn min_3_int<T: Ord>(a: T, b: T, c: T) -> T {
    std::cmp::min(std::cmp::min(a, b), c)
}
fn max_3_int<T: Ord>(a: T, b: T, c: T) -> T {
    std::cmp::max(std::cmp::max(a, b), c)
}

fn min_2_int<T: Ord>(a: T, b: T) -> T {
    std::cmp::min(a, b)
}

// function that "set stuff" in the drawing buffer; assuming its a double raster
fn set_pixel_double_weights<DEPTHACC: Real, const DEPTHCOUNT: usize>(
    prim_ref: &PrimitivReferences,
    drawing_buffer: &mut DrawBuffer<DEPTHCOUNT, DEPTHACC>,
    depth: DEPTHACC,
    col: usize,
    row: usize,
    u0: f32,
    v0: f32,
    u1: f32,
    v1: f32,
) {
    let w = TVec2::new(u0, v0);
    let w_alt = TVec2::new(u1, v1);
    drawing_buffer.set_depth_content(
        row,
        col,
        depth,
        w,
        w_alt,
        prim_ref.node_id,
        prim_ref.geometry_id,
        prim_ref.material_id,
        prim_ref.primitive_id,
    );
}

fn barycentric_coord(
    pa: &PointInfo<f32>,
    pb: &PointInfo<f32>,
    pc: &PointInfo<f32>,
    row: usize,
    col: usize,
) -> (f32, f32, f32) {
    let pa_col = pa.p.y;
    let pa_row = pa.p.x;
    let pb_col = pb.p.y;
    let pb_row = pb.p.x;
    let x3 = pc.p.y;
    let y3 = pc.p.x;
    let p_col = col as f32;
    let p_row = row as f32;

    // calculate the bar
    let denom = (pb_row - y3) * (pa_col - x3) + (x3 - pb_col) * (pa_row - y3);
    let w1 = ((pb_row - y3) * (p_col - x3) + (x3 - pb_col) * (p_row - y3)) / denom;
    let w2 = ((y3 - pa_row) * (p_col - x3) + (pa_col - x3) * (p_row - y3)) / denom;

    // that way of doing the calculation might be more stable on the edges
    let w3 = 1.0 - w1 - w2;
    //let w3 = ((pa_row - pb_row) * (p_col - pa_col) + (pb_col - pa_col) * (p_row - pa_row)) / denom;

    (w1, w2, w3)
}
fn barycentric_coord_shift(
    pa: &PointInfo<f32>,
    pb: &PointInfo<f32>,
    pc: &PointInfo<f32>,
    lower_shift: f32,
    row: usize,
    col: usize,
) -> (f32, f32, f32) {
    let x1 = pa.p.y;
    let y1 = pa.p.x;
    let x2 = pb.p.y;
    let y2 = pb.p.x;
    let x3 = pc.p.y;
    let y3 = pc.p.x;
    let px = col as f32;
    let py = (row as f32) + lower_shift;

    let denom = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3);
    let w1 = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denom;
    let w2 = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denom;
    let w3 = 1.0 - w1 - w2;

    (w1, w2, w3)
}

pub fn raster_element<const DEPTHCOUNT: usize, const VERTEX_COUNT: usize>(
    element: &PrimitiveElements,
    _vertexbuffer: &VertexBuffer<VERTEX_COUNT>,
    drawing_buffer: &mut DrawBuffer<DEPTHCOUNT, f32>,
) {
    match element {
        PrimitiveElements::Line { fds, pa, pb, uv } => {
            raster_line(drawing_buffer, fds, pa, pb);
        }
        PrimitiveElements::Point { fds, point, uv: _ } => {
            raster_point_info(drawing_buffer, fds, point);
        }
        PrimitiveElements::Triangle(t) => {
            raster_triangle(drawing_buffer, &t.primitive_reference, &t.pa, &t.pb, &t.pc);
        }
        PrimitiveElements::Triangle3D(t) => {
            // raster_triangle(drawing_buffer, &t.primitive_reference, &t.pa, &t.pb, &t.pc);
            tomato_draw_triangle(drawing_buffer, &t.primitive_reference, &t.pa, &t.pb, &t.pc)
        }

        PrimitiveElements::Static { fds: _, index: _ } => todo!(),
    }
}

pub fn raster_all<const DEPTHCOUNT: usize, const VERTEX_COUNT: usize>(
    primitivbuffer: &PrimitiveBuffer,
    vertexbuffer: &VertexBuffer<VERTEX_COUNT>,
    drawing_buffer: &mut DrawBuffer<DEPTHCOUNT, f32>,
) {
    for primitiv_idx in 0..primitivbuffer.current_size {
        let element = primitivbuffer.content[primitiv_idx];

        raster_element(&element, vertexbuffer, drawing_buffer)
    }
}

#[pyfunction]
pub fn raster_all_py(
    _py: Python,
    pb: &PrimitiveBufferPy,
    vbuffpy: &VertexBufferPy,
    mut db: PyRefMut<'_, AbigDrawing>,
) {
    let primitivbuffer = &pb.content;

    let drawing_buffer = &mut db.db;
    raster_all(primitivbuffer, &vbuffpy.buffer, drawing_buffer);
}
