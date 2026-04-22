import mongoose from "mongoose";
import bcrypt from "bcryptjs";

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      maxlength: 50,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      index: true
    },
    password: {
      type: String,
      required: true,
      minlength: 6,
      select: false,
    },
    about: {
      type: String,
    },
    role: {
      type: String,
      enum: ["user", "admin"],
      default: "user",
    },
    isActive: {
      type: Boolean,
      default: true,
      index: true
    },
    isDeleted:{
      type:Boolean,
      default:false
    },
    deletedAt:{
      type:Date,
      default:null
    }
  },
  { timestamps: true }
);


userSchema.index({ name: "text", email: "text" });

// Hash password
userSchema.pre("save", async function () {
  if (!this.isModified("password")) return

  this.password = await bcrypt.hash(this.password, 12);
});


//hide deeted users

userSchema.pre(/^find/, function (next) {

  this.where({ isDeleted: false });

});

// Compare password
userSchema.methods.comparePassword = async function (userPassword) {
  return await bcrypt.compare(userPassword, this.password);
};

export default mongoose.model("User", userSchema);