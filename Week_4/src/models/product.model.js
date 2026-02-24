import mongoose from "mongoose";
import {nanoid} from "nanoid";
import slugify from "slugify";

const productSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: true,
      trim: true,
    },
    slug: {
      type: String,
      unique: true,
      index: true,
      required:true
    },
    description: {
      type: String,
    },
    category: {
      type: String,
      required: true,
    },
    price: {
      type: Number,
      required: true,
    },
    brand: {
      type: String,
      required: true,
      trim: true,
    },
    stock: {
      type: Number,
      required: true,
      min: 0,
      default: 0,
    },
    ratingsAverage: {
      type: Number,
      min: 1,
      max: 5,
      default: 4,
    },
    ratingsQuantity: {
      type: Number,
      default: 0,
    },
    isActive: {
      type: Boolean,
      default: true,
    },
    createdBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
    },
    minPrice:{
      type:Number,
      required:true
    },
    maxPrice:{
      type:Number,
      required:true
    },
    
  },
  { timestamps: true },
);

// For save
productSchema.pre("validate", function (next) {
  if (this.isModified("title")) {
    const baseSlug = slugify(this.title, { lower: true, strict: true });
    this.slug = `${baseSlug}-${nanoid(6)}`
  }
  
  // next();
});

// For update
productSchema.pre("findOneAndUpdate", function (next) {
  const update = this.getUpdate();

  if (update.title) {
    const baseSlug = slugify(update.title, {lower: true, strict: true});
    update.slug = `${baseSlug}-${nanoid(6)}`;
  }

  // next();
});

productSchema.virtual("ratingPercentage").get(function () {
  return (this.ratingsAverage / 5) * 100;
});

productSchema.set('toJSON', {
  virtuals: true 
});

const Product = mongoose.model("Product", productSchema);

export default Product;
