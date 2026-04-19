import { z } from "zod";

export const UserSchema = z.object({
  id:        z.number(),
  email:     z.string().email(),
  firstName: z.string(),
  lastName:  z.string(),
  phone:     z.string().optional(),
  avatar:    z.string().nullable(),
  role:      z.enum(["customer", "admin", "staff"]),
  isActive:  z.boolean(),
  createdAt: z.string().datetime(),
});

export const LoginSchema = z.object({
  email:    z.string().email("Email không hợp lệ"),
  password: z.string().min(8, "Mật khẩu tối thiểu 8 ký tự"),
});

export const RegisterSchema = LoginSchema.extend({
  firstName:       z.string().min(1, "Vui lòng nhập tên"),
  lastName:        z.string().min(1, "Vui lòng nhập họ"),
  confirmPassword: z.string(),
}).refine((d) => d.password === d.confirmPassword, {
  message: "Mật khẩu không khớp",
  path:    ["confirmPassword"],
});

export const AuthTokenSchema = z.object({
  access:  z.string(),
  refresh: z.string(),
});

export type User          = z.infer<typeof UserSchema>;
export type LoginInput    = z.infer<typeof LoginSchema>;
export type RegisterInput = z.infer<typeof RegisterSchema>;
export type AuthToken     = z.infer<typeof AuthTokenSchema>;
