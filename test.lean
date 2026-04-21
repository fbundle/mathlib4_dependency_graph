variable (CommRingCat : Type (u + 1))
variable (Opposite : Sort u → Sort (max 1 u))
variable (AlgebraicGeometry_dot_Scheme_dot_instCategory : CategoryTheory_dot_Category.{u_1, u_1 + 1} AlgebraicGeometry_dot_Scheme)
variable (AlgebraicGeometry_dot_Scheme_dot_Spec : CategoryTheory_dot_Functor CommRingCatᵒᵖ AlgebraicGeometry_dot_Scheme)
variable (CategoryTheory_dot_Functor_dot_EssSurj_dot_toEssImage : ∀ {C : Type u₁} {D : Type u₂} [inst : CategoryTheory_dot_Category.{v₁, u₁} C] [inst_1 : CategoryTheory_dot_Category.{v₂, u₂} D]
  {F : CategoryTheory_dot_Functor C D}, F_dot_toEssImage_dot_EssSurj)
variable (AlgebraicGeometry_dot_instCategoryAffineScheme : CategoryTheory_dot_Category.{u_1, u_1 + 1} AlgebraicGeometry_dot_AffineScheme)
variable (AlgebraicGeometry_dot_Scheme : Type (u_1 + 1))
variable (CategoryTheory_dot_Functor_dot_EssSurj : {C : Type u₁} →
  {D : Type u₂} →
    [inst : CategoryTheory_dot_Category.{v₁, u₁} C] →
      [inst_1 : CategoryTheory_dot_Category.{v₂, u₂} D] → CategoryTheory_dot_Functor C D → Prop)
variable (AlgebraicGeometry_dot_AffineScheme : Type (u_1 + 1))
variable (CategoryTheory_dot_Category_dot_opposite : {C : Type u₁} → [CategoryTheory_dot_Category.{v₁, u₁} C] → CategoryTheory_dot_Category.{v₁, u₁} Cᵒᵖ)
variable (CommRingCat_dot_instCategory : CategoryTheory_dot_Category.{u_1, u_1 + 1} CommRingCat)
variable (AlgebraicGeometry_dot_AffineScheme_dot_Spec : CategoryTheory_dot_Functor CommRingCatᵒᵖ AlgebraicGeometry_dot_AffineScheme)
def AlgebraicGeometry_dot_AffineScheme_dot_Spec_essSurj : AlgebraicGeometry_dot_AffineScheme_dot_Spec_dot_EssSurj := sorry
