#version 330

in layout(location = 0) vec3 position;
in layout(location = 1) vec2 inTexCoords;
in layout(location = 2) vec3 normals;

uniform mat4 projection_matrix;
uniform mat4 transform_model_view_matrix;


out vec2 outTexCoords;
out vec3 surfaceNormal;

void main()
{
    surfaceNormal = (transform_model_view_matrix * vec4(normals, 0.0f)).xyz;
    gl_Position = projection_matrix * transform_model_view_matrix * vec4(position, 1.0f);
    outTexCoords = inTexCoords;
}