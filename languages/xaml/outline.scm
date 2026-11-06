(element
  (STag
    (Name) @name)) @item

(EmptyElemTag
  (Name) @name) @item

; x:Name is listed as a child of its element, so named elements can be found by searching the outline.
(Attribute
  (Name) @context
  (AttValue) @name
  (#match? @context "^(x:)?Name$")) @item
